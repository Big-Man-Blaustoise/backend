from django.core.management.base import BaseCommand
from django.urls import URLPattern, URLResolver, get_resolver
from django.conf import settings

class Command(BaseCommand):
    help = 'Generate backend API documentation for the frontend team'

    def handle(self, *args, **kwargs):
        # Fetch all URL patterns from the project
        url_patterns = self.get_all_url_patterns()
        
        # Prepare documentation list
        docs = []

        # Loop through the patterns and compile details
        for pattern in url_patterns:
            view = pattern.callback

            # Check if the view is a class-based view (CBV) or function-based view (FBV)
            if hasattr(view, 'view_class'):  # CBV
                view_name = f'{view.view_class.__module__}.{view.view_class.__name__}'
                methods = ', '.join([method.upper() for method in view.http_method_names])
            else:  # FBV
                view_name = str(view.__name__)
                # Function-based views generally support 'GET', 'POST', etc.
                methods = 'GET, POST'  # You could expand this to reflect the actual methods

            # Build the URL and description
            docs.append({
                'url': pattern.pattern,
                'view': view_name,
                'methods': methods,
                'description': view.__doc__ if hasattr(view, '__doc__') else 'No description available',
            })

        # Print the documentation
        self.print_documentation(docs)

    def get_all_url_patterns(self):
        """
        Recursively retrieves all URL patterns from the project and apps.
        """
        url_patterns = []
        resolver = get_resolver()
        for pattern in resolver.url_patterns:
            if isinstance(pattern, URLResolver):
                url_patterns.extend(self.get_url_patterns_from_resolver(pattern))
            elif isinstance(pattern, URLPattern):
                url_patterns.append(pattern)
        return url_patterns

    def get_url_patterns_from_resolver(self, resolver):
        """
        Helper function to retrieve patterns from URLResolver objects.
        """
        url_patterns = []
        for pattern in resolver.url_patterns:
            if isinstance(pattern, URLResolver):
                url_patterns.extend(self.get_url_patterns_from_resolver(pattern))
            elif isinstance(pattern, URLPattern):
                url_patterns.append(pattern)
        return url_patterns

    def print_documentation(self, docs):
        """
        Prints out the API documentation in a readable format.
        """
        self.stdout.write('API Documentation\n')
        self.stdout.write('-' * 80)
        for doc in docs:
            self.stdout.write(f'URL: {doc["url"]}')
            self.stdout.write(f'  View: {doc["view"]}')
            self.stdout.write(f'  Methods: {doc["methods"]}')
            self.stdout.write(f'  Description: {doc["description"]}\n')

        self.stdout.write('-' * 80)
        self.stdout.write(f'Total API Endpoints: {len(docs)}\n')
