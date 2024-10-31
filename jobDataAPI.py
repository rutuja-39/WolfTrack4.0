import requests
import urllib.parse

class JobDataAPI:
    def __init__(self, api_url, app_id, app_key):
        """
        Initialize the JobDataAPI class with an API URL, app ID, and app key.
        :param api_url: Base URL of the API
        :param app_id: Application ID for authentication
        :param app_key: Application key for authentication
        """
        self.api_url = api_url
        self.app_id = app_id
        self.app_key = app_key

    def getJobDataByPref(self, preferences):
        """
        Get job data based on user preferences by making an API request.
        :param preferences: Dictionary containing user preferences (e.g., location, industry)
        :return: Response data from the API containing job data matching preferences
        """
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            **preferences
        }
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def getSalaryHistogram(self):
        """
        Get salary histogram data for jobs by making an API request.
        :return: Response data from the API containing salary histogram
        """
        # Assuming the API supports this endpoint for salary histogram data
        response = requests.get(f"{self.api_url}/salary_histogram", params={"app_id": self.app_id, "app_key": self.app_key})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def getHistoricalSalary(self, job_title):
        """
        Get historical salary data for a specific job title by making an API request.
        :param job_title: Job title for which historical salary data is needed
        :return: Response data from the API containing historical salary data
        """
        # Assuming the API supports this endpoint for historical salary data
        response = requests.get(f"{self.api_url}/historical_salary", params={"app_id": self.app_id, "app_key": self.app_key, "job_title": job_title})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def getJobGeoData(self, location):
        """
        Get geographical data for jobs in a specific location by making an API request.
        :param location: Location for which job geographical data is needed
        :return: Response data from the API containing geographical job data
        """
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "location": location
        }
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def getTopCompanies(self, limit=10):
        """
        Get the top companies by the number of job postings by making an API request.
        :param limit: Number of top companies to return
        :return: Response data from the API containing top companies and their job posting counts
        """
        # Assuming the API supports this endpoint for top companies data
        response = requests.get(f"{self.api_url}/top_companies", params={"app_id": self.app_id, "app_key": self.app_key, "limit": limit})
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

# Example usage
app_id = "575e7a4b"
app_key = "35423835cbd9428eb799622c6081ffed"
api_url = "https://api.adzuna.com/v1/api/jobs/us/search/1?"

api = JobDataAPI(api_url, app_id, app_key)


params = {'location0': 'New York', 'category': 'Tech', 'what_phrase': 'Software Engineer'}
encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
print(encoded_params)

job_data = api.getJobDataByPref(encoded_params)
print(job_data)
