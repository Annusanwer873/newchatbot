# -*- coding: utf-8 -*-
class TemplateReader:
    def __init__(self):
        pass

    def read_course_template(self,course_name):
        try:
            #email_file = open("email_templates/DSM_Template.html", "r")
            if (course_name == 'ComputerScience'):
                email_file = open("email_templates/CS_email_template.html", "r")
                email_message = email_file.read()
                return email_message

            elif (course_name == 'BuisnessAdminstration'):
                email_file = open("email_templates/BBA_email_template.html", "r")
                email_message = email_file.read()
                return email_message

            elif (course_name == 'MediaScience'):
                email_file = open("email_templates/Media_email_template.html", "r")
                email_message = email_file.read()
                return email_message



            # if (course_name=='DataScienceMasters'):
            #     email_file = open("email_templates/DSM_Template.html", "r")
            #     email_message = email_file.read()
            # elif (course_name=='MachineLearningMasters'):
            #     email_file = open("email_templates/MLM_Template.html", "r")
            #     email_message = email_file.read()
            # elif (course_name == 'DeepLearningMasters'):
            #     email_file = open("email_templates/DLM_Template.html", "r")
            #     email_message = email_file.read()
            # elif (course_name == 'NLPMasters'):
            #     email_file = open("email_templates/NLPM_Template.html", "r")
            #     email_message = email_file.read()
            # elif (course_name == 'DataScienceForManagers'):
            #     email_file = open("email_templates/DSFM_Template.html", "r")
            #     email_message = email_file.read()
            # elif (course_name == 'Vision'):
            #     email_file = open("email_templates/Vision_Template.html", "r")
            #     email_message = email_file.read()
            # return email_message
        except Exception as e:
            print('The exception is '+str(e))



