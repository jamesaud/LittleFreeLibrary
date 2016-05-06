from wikiblog.models import Hashtag
from wikiblog.utilities import names

def initializeWikiblog():
    hashtag_all = Hashtag(tag="tesgintaeras")
    hashtag_all.save()

    names.CreateNames("random_names.txt")
