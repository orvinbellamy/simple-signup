# simple-signup

Project link: https://github.com/orvinbellamy/simple-signup
Contributor: Orvin Bellamy (https://github.com/orvinbellamy)

Last update: 3rd June 2025

Python 3.9.13

## About The Project

Trying out a very simple web development from someone who's been in analytics. Wanted to try building a simple web application using AWS (not a very good idea).

The web application is inspired from my time playing badminton where people hosts badminton sessions, and players can sign up. This is usually done on Whatsapp or Facebook groups. Hosts can create sessions on the website, and players can signup without needing to login with an account.

The website is hosted on AWS CloudFront and S3 (static hosting), and the data stored on DynamoDB. API Gateway is used to create API routes, which triggers Lambda functions to send data between DynamoDB and the web page.

Some features include:
- REST(ful) API
- API Gateway throttling protection
- Header authorization via CloudFront and Lambda

## How To Use

Go to https://d2mgloh4y05lpj.cloudfront.net and login with the username "obellamy". No feature to create new accounts as this is just for a demo.