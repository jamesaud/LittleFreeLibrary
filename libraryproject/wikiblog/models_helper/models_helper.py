from wikiblog.models import Random_name

#Total number of page comments
from wikiblog.models import Page, Comment

class PageCalc():
    def total_page_comments(self, Page):
        if not Page.comment_set.all():
            return 0
        else:
            total = 0
            for comment in Page.comment_set.all():
                total += 1 + self.total_sub_comments(comment)
            return total

    #Calculates total sub comments
    def total_sub_comments(self, comment):
        if not comment.comment_set.all():
            return 0
        else:
            return len(comment.comment_set.all()) + sum([self.total_sub_comments(comm) for comm in comment.comment_set.all()])


