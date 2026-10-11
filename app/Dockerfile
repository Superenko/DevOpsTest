FROM python:3.12-alpine
WORKDIR /app
COPY server.py .
RUN adduser -D -u 10001 appuser
USER appuser
EXPOSE 8080
CMD ["python", "-u", "server.py"]