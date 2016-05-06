from wikiblog.models import User, User_page_accessed
import os

base_dir = "statistics/"

class UserStats():
    #Takes in a User Model, writes stats about ...
    def write_user_stats(self, User, filename):
        with open(base_dir+filename, 'w') as stats:
            username = User.user_name
            user_id = User.id
            pages_accessed = User.user_page_accessed_set.all()

            #upa is a user_page_accessed object
            #store a list of lists, all the the upa data to write
            upa_data=[]

            for upa in pages_accessed:
                upa_data.append([upa.url,upa.referring_url,str(upa.date_accessed),str(upa.id)])
            
                
            stats.write(username + " | id = " + str(user_id))
            stats.write("\n")
            stats.write("*" * 4)
            stats.write("\n")
            
            for upa_list in upa_data:
                try:
                    stats.write("URL: " + upa_list[0] + "\nREFFERING URL: " + upa_list[1] + "\nDATE ACCESSED: " + upa_list[2] + "\nID: " + upa_list[3])
                    stats.write("\n\n")
                except:
                    pass
                
            stats.write("*" * 20)


def runtest():
    user = User.objects.get(user_name="Damaged Magpie")
    us = UserStats()
    us.write_user_stats(user, user.user_name+".txt")
    
