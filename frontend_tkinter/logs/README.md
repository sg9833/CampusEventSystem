# Log Directory

This directory contains application log files:

- **app.log** - All application logs (INFO and above)
- **error.log** - Error and critical logs only
- **api.log** - API request/response logs
- **audit.log** - User action audit trail

## Log Rotation

Logs are automatically rotated when they reach 10 MB.
Up to 5 backup files are kept for each log type.

## Viewing Logs

**View logs in real-time:**
```bash
# Application logs
tail -f logs/app.log

# Error logs
tail -f logs/error.log

# API logs
tail -f logs/api.log

# Audit logs
tail -f logs/audit.log
```

**Search logs:**
```bash
# Find errors
grep ERROR logs/app.log

# Find specific user actions
grep "username" logs/audit.log

# Find API calls to specific endpoint
grep "/events" logs/api.log
```

## Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages (application continues)
- **ERROR**: Error messages (feature fails but app continues)
- **CRITICAL**: Critical errors (application may stop)

## Log Retention

Logs are kept according to the rotation policy:
- Current log file + 5 backups
- Each file up to 10 MB
- Total ~60 MB per log type

## Privacy

Audit logs contain user actions. Ensure proper access controls:
```bash
chmod 600 logs/audit.log
```

## Troubleshooting

If logs are not being created:
1. Check directory permissions: `ls -la logs/`
2. Ensure LOG_LEVEL is set in config.ini or .env
3. Check application has write permissions
4. Review console output for logging errors
