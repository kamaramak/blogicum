from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        pk = self.kwargs['pk']
        return redirect(reverse(
            'blog:post_detail',
            kwargs={'pk': pk}
        ))