from linkedin_interface import LinkedInInterface


linkedin_interface = LinkedInInterface()

linkedin_interface.check_for_login_page()

linkedin_interface.evaluate_job_listings()

linkedin_interface.terminate_driver()
