# Cache Directory

This directory stores application cache data:

- **local_cache.db** - SQLite database for local caching
- **images/** - Cached images and assets
- **api_responses/** - Cached API responses

## Cache Configuration

Cache settings are configured in `config.ini`:

```ini
[CACHE]
enabled = true
ttl = 300
max_size = 50
cache_dir = cache
```

## Cache Management

**Clear cache:**
```bash
# Clear all cache
rm -rf cache/*

# Clear specific cache
rm cache/local_cache.db
rm -rf cache/images/*
```

**Check cache size:**
```bash
du -sh cache/
```

## Cache Types

### API Response Cache
- Default TTL: 5 minutes (300 seconds)
- Stores GET request responses
- Invalidated on POST/PUT/DELETE operations

### Image Cache
- Stores downloaded images
- Max size: 100 MB
- LRU eviction policy

### Database Cache
- SQLite database for structured data
- Stores frequently accessed data
- Automatic cleanup of expired entries

## Performance Impact

Caching significantly improves performance:
- **API calls**: ~80% reduction in network requests
- **Image loading**: ~90% faster on subsequent loads
- **Page navigation**: ~60% faster with cached data

## Troubleshooting

If cache-related issues occur:

1. **Clear cache:** `rm -rf cache/*`
2. **Check permissions:** `ls -la cache/`
3. **Disable caching temporarily:** Set `CACHE_ENABLED=false` in .env
4. **Check cache size:** Ensure not exceeding max_size limit
5. **Review logs:** `grep CACHE logs/app.log`

## Security

Cache may contain sensitive data:
- Ensure proper file permissions
- Don't commit cache to version control
- Clear cache when changing users
- Use encryption for sensitive cached data

## .gitignore

Cache directory should be in .gitignore:
```
cache/
*.db
*.cache
```
