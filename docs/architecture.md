# Architecture

The system provides REST API endpoints:
+ To make reservations
+ To check if a number of rooms are available at a certain time

Project features:
+ Soft delete
+ Tuned queries to prevent duplicates in bulk insert
+ The listing owner can get an overview of the booked rooms on admin panel
+ API documentaion on /swagger/ and /redoc/