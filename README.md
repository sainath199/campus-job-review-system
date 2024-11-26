 # Campus Job Review System
 
<!-- <a href="https://github.com/sainath199/campus-job-review-system/actions" alt="Build Status"><img src="https://img.shields.io/github/workflow/status/github.com/sainath199/campus-job-review-system/Build%20main" /></a> -->
<!-- 
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/user-attachments/assets/website?color=magenta&label=Documentation)
-->
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14027357.svg)](https://doi.org/10.5281/zenodo.14027357)
<a href="https://github.com/sainath199/campus-job-review-system/blob/main/LICENSE">
  <img alt="License" src="https://img.shields.io/github/license/sainath199/campus-job-review-system">
</a>
[![GitHub Release](https://img.shields.io/github/release/sainath199/campus-job-review-system.svg)](https://github.com/sainath199/campus-job-review-system/releases) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test and Formatting](https://github.com/sainath199/campus-job-review-system/actions/workflows/test.yml/badge.svg)](https://github.com/sainath199/campus-job-review-system/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/sainath199/f90d8ff63781978b73c28561177358b3/raw/coverage.json)](https://github.com/sainath199/campus-job-review-system/actions/workflows/test.yml)
[![Static Code Analysis](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/sainath199/6e6740fb4d21afa29af5a1eba71cedba/raw/Static_code_analysis.json)](https://github.com/sainath199/campus-job-review-system/actions/workflows/test.yml)
[![Security Scans](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/sainath199/e9d969e042f2cc3e639dbac2a074ba92/raw/Security_scan.json)](https://github.com/sainath199/campus-job-review-system/actions/workflows/test.yml)


![Campus Job Review System](https://github.com/sainath199/campus-job-review-system/blob/main/new_campus_job_review.png)

The Campus Job Review System is a Flask App which has a SQL database for storage. It is created using Python.This website allows NCSU students to read reviews of any job that is open on campus. The portal's objective is to assist students in better comprehending the job description and the work through the experiences of their fellow students. Students can post reviews on the website for others to read. The pupils' anonymity is preserved so they can submit candid evaluations. Furthermore, the website offers user account management, allowing users to store their Resume and contact details. Only that specific user can modify these details after logging in (using the Account Page).

- Read reviews of on-campus jobs posted by peers.
- Post reviews of jobs to share their experiences.
- Apply for on-campus jobs and track their application statuses.
- Receive notifications about newly added job opportunities.
- Analyze job reviews through comprehensive analytics.
- Provide feedback to improve the platform.
With a SQL database for storage, this system preserves the anonymity of reviews while ensuring user account security and resume management.

## What's New?
The Campus Job Review System now includes these exciting features:

- Job Application Management: Users can apply for jobs directly and track application statuses.
- Job Tracker: Displays all jobs applied for along with their statuses.
- Notifications: Alerts users when new jobs are added to the system.
- Job Review Analytics: Provides insightful analytics for job reviews, including average ratings and review counts.
- Feedback System: Enables users to submit feedback to improve the platform.

 <b>Feature 1 - Real time tracking of application status</b>
 <br>
 <img src="feature1.png" alt="Sample Image" width="600">

 <b>Feature 2 - Implemented a Feedback page</b>
 <br>
 <img src="feature2.png" alt="Sample Image" width="600">
 
 <b>Feature 3 - User Review Statistics </b>
 <br>
 <img src="feature3.png" alt="Sample Image" width="600">
 
 <b>Feature 4 - Notifications and alerts</b>
 <br>
 <img src="feature4.png" alt="Sample Image" width="600">
 

## Pre-requisites
To execute these scripts, your computer must have Python installed. For the latest Python version, please visit [Python Installers](https://www.python.org/downloads/). You can use requirements.txt to install other requirements in addition to that. The requirements.txt file has been updated in light of the advancements made.

## Installation
Initially you can check whether your system has python pre-installed or not, usually nowadays in most of the systems, be it Windows or MacOS, python is pre-installed. 

To check whether you have python installed or not, you can open CMD or a Terminal and run the command "python --version". If the CMD shows the version such as Python 3.6.7 then your system already has python installed and you just need to clone the repository and run the python scripts. 

If this is not the case, then you need to download python installer package from [Python Installers](https://www.python.org/downloads/) based on your system's operating system and install it and you can further clone this repository to execute the scripts.

You can refer [Install.md](https://github.com/sainath199/campus-job-review-system/blob/main/install.md) for the complete installation steps based on your OS.


## Demo Video


[![Watch the Demo](https://img.youtube.com/vi/ShoX_AONV6I&ab/0.jpg)](https://www.youtube.com/watch?v=ShoX_AONV6I&ab_channel=MonaSreeMuppala)

## Usage
Here’s an overview of some key features:

- Apply for Jobs: View job listings and apply directly.
- Track Applications: Monitor the status of your job applications.
- Post Job Reviews: Share your experiences and insights about on-campus jobs.
- Analyze Job Reviews: Get a detailed analysis of reviews with charts and scores.
- Manage Your Profile: Update contact information and upload resumes securely.
- Notifications: Stay updated with alerts on newly posted jobs.
- Provide Feedback: Use the feedback page to share suggestions or report issues.

## Testing

We use pytest to perform testing on all unit tests together. The command needs to be run from the home directory of the project. The command is:
```
python -m pytest test/
```

## Code Coverage

Code coverage is part of the build. Every time new code is pushed to the repository, the build is run, and along with it, code coverage is computed. This can be viewed by selecting the build, and then choosing the codecov pop-up on hover.

Locally, we use the coverage package in python for code coverage. The commands to check code coverage in python are as follows:

```
coverage run -m pytest test/
coverage report
```

Please note: A coverage below 70% will cause the build to fail.

## Who Should Use Campus job review system?
This platform is ideal for:

- Students: Looking for on-campus job opportunities and reviews to make informed decisions.
- Job Seekers: Wanting to track their job applications and receive notifications on new opportunities.
- Reviewers: Sharing their experiences with peers in a secure, anonymous manner.
- Administrators: Managing job postings and analyzing feedback for continuous improvement.

## What More Can Be Done?
Check out the issue list here to explore potential improvements and contribute to the project.

## Troubleshooting

- Database Issues: Ensure database migrations are set up correctly with flask db upgrade.
- Environment Errors: Check if the FLASK_APP variable is set properly and your virtual environment is activated.
- Dependency Issues: Run pip install -r requirements.txt to ensure all dependencies are installed.
- Server Access Issues: Use --host=0.0.0.0 when running the Flask app to access it externally.

## Contributing
Contributions are welcome! Please read the CONTRIBUTING.md for more details.

- Fork the repository and create a new branch.
- Submit a pull request with a description of changes.
- Test Coverage: Ensure changes pass all tests and maintain 70%+ coverage.

## License
- This project is licensed under the MIT License. See the LICENSE file for details.

### Chat Channel Screenshot

![image](chat.png)

## Contributors

- [Mona Sree Muppala](https://github.com/Monasree)
- [Sainath Gorige](https://github.com/sainath199)
- [Vishal Reddy Devireddy](https://github.com/vishalreddy2323)
