from django.core import paginator


class PaginatorMixin:
    objects_per_page = 10

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        objects = self.get_ordered_children()
        paginator_obj = paginator.Paginator(objects, self.objects_per_page)
        page_number = request.GET.get('p', 1)

        try:
            page = paginator_obj.page(page_number)
        except paginator.PageNotAnInteger:
            page = paginator_obj.page(1)
        except paginator.EmptyPage:
            page = paginator_obj.page(paginator_obj.num_pages)

        context.update({
            'paginator_page': page,
        })

        return context

    def get_ordered_children(self):
        return self.get_children().live().specific()
