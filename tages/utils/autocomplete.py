from django.http import JsonResponse
from django.views.generic.list import BaseListView


class AutocompleteJsonView(BaseListView):
    """Handle AutocompleteWidget's AJAX requests for data."""
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        """
        Return a JsonResponse with search results of the form:
        {
            results: [{id: "123" text: "foo"}],
            pagination: {more: true}
        }
        """
        self.term = request.GET.get('term', '')
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse(dict(
            results=[
                dict(id=str(obj.pk), text=self.get_result_label(obj))
                for obj in context['object_list']
            ],
            pagination=dict(more=context['page_obj'].has_next()),
        ))

    def get_result_label(self, obj):
        return str(obj)

    def get_queryset(self):
        msg = 'subclasses of AutocompleteJsonView must provide a ' \
            'get_queryset() method'
        raise NotImplementedError(msg)
