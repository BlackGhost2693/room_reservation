# Room Reservation Application

## Project Description:
A system for making and tracking reservations that can be handled by third-party services.

## Project Documentations
- [deployment](docs/deployment.md)
- [installation](docs/installation.md)
- [architecture](docs/architecture.md)

## <mark>Note</mark>
This repo contains two different architectures:
- `main` branch: date-separated reservations
- `daterange_reservation` branch: from_date until to_date reservations

## Article
[link](https://medium.com/@amirayat20/django-rest-efficient-bulk-create-d2fea0ad3e54)

## Project routes
- http://127.0.0.1:8000/swagger/                
- http://127.0.0.1:8000/redoc/
- http://127.0.0.1:8000/room/available/?from_ts={timestamp}&to_ts={timestamp}/
- http://127.0.0.1:8000/room/available/{room_number}/?from_ts={timestamp}&to_ts={timestamp}/
- http://127.0.0.1:8000/room/reserve/
- http://127.0.0.1:8000/admin/rooms/room/
- http://127.0.0.1:8000/admin/rooms/reservation/
