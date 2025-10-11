"""
Configuration System Demo
Demonstrates all features of the unified configuration management
"""

from config.settings import settings, get_settings, reload_settings


def demo_basic_access():
    """Demo: Basic configuration access"""
    print("\n" + "="*60)
    print("1. BASIC ACCESS PATTERNS")
    print("="*60)
    
    # Method 1: Attribute access
    print(f"API URL (attribute): {settings.API_BASE_URL}")
    
    # Method 2: Dictionary access
    print(f"API URL (dict):      {settings['API_TIMEOUT']}")
    
    # Method 3: Get method with default
    print(f"Custom key (get):    {settings.get('CUSTOM_KEY', 'default')}")


def demo_all_config():
    """Demo: View all configuration"""
    print("\n" + "="*60)
    print("2. ALL CONFIGURATION VALUES")
    print("="*60)
    
    # Print first 15 config values
    config_dict = settings.to_dict()
    for i, (key, value) in enumerate(sorted(config_dict.items())):
        if i >= 15:
            print(f"... and {len(config_dict) - 15} more")
            break
        print(f"{key:35} = {value}")


def demo_environment_detection():
    """Demo: Environment detection"""
    print("\n" + "="*60)
    print("3. ENVIRONMENT DETECTION")
    print("="*60)
    
    print(f"Current environment:  {settings.env}")
    print(f"Is Development?       {settings.is_development()}")
    print(f"Is Production?        {settings.is_production()}")
    print(f"Is Testing?           {settings.is_testing()}")


def demo_categories():
    """Demo: Configuration by category"""
    print("\n" + "="*60)
    print("4. CONFIGURATION BY CATEGORY")
    print("="*60)
    
    print("\n📡 API Configuration:")
    print(f"  Base URL:     {settings.API_BASE_URL}")
    print(f"  Timeout:      {settings.API_TIMEOUT}s")
    print(f"  Retries:      {settings.API_RETRY_ATTEMPTS}")
    
    print("\n💾 Cache Configuration:")
    print(f"  Enabled:      {settings.CACHE_ENABLED}")
    print(f"  TTL:          {settings.CACHE_TTL}s")
    print(f"  Max Size:     {settings.CACHE_MAX_SIZE}")
    
    print("\n📝 Logging Configuration:")
    print(f"  Level:        {settings.LOG_LEVEL}")
    print(f"  Directory:    {settings.LOG_DIR}")
    print(f"  Max Size:     {settings.LOG_MAX_SIZE} bytes")
    
    print("\n🔒 Session Configuration:")
    print(f"  Timeout:      {settings.SESSION_TIMEOUT}s")
    print(f"  Warning:      {settings.SESSION_WARNING_TIME}s")
    print(f"  Persistent:   {settings.SESSION_PERSISTENT}")
    
    print("\n🎨 UI Configuration:")
    print(f"  Theme:        {settings.UI_THEME}")
    print(f"  Window Size:  {settings.UI_WINDOW_WIDTH}x{settings.UI_WINDOW_HEIGHT}")
    print(f"  Font:         {settings.UI_FONT_FAMILY} {settings.UI_FONT_SIZE}pt")
    
    print("\n⚡ Performance Configuration:")
    print(f"  Lazy Load:    {settings.PERFORMANCE_LAZY_LOADING}")
    print(f"  Monitoring:   {settings.PERFORMANCE_MONITORING}")
    print(f"  Page Size:    {settings.PERFORMANCE_PAGE_SIZE}")


def demo_runtime_changes():
    """Demo: Runtime configuration changes"""
    print("\n" + "="*60)
    print("5. RUNTIME CONFIGURATION CHANGES")
    print("="*60)
    
    print(f"Original timeout: {settings.API_TIMEOUT}")
    
    # Change at runtime
    settings.set('API_TIMEOUT', 60)
    print(f"Modified timeout: {settings.API_TIMEOUT}")
    
    # Add custom key
    settings.set('MY_CUSTOM_KEY', 'custom_value')
    print(f"Custom key:       {settings.get('MY_CUSTOM_KEY')}")


def demo_helper_functions():
    """Demo: Helper functions"""
    print("\n" + "="*60)
    print("6. HELPER FUNCTIONS")
    print("="*60)
    
    from config.settings import get_api_base_url, get_cache_dir, get_log_dir
    
    print(f"API Base URL:     {get_api_base_url()}")
    print(f"Cache Directory:  {get_cache_dir()}")
    print(f"Log Directory:    {get_log_dir()}")


def demo_feature_flags():
    """Demo: Feature flags"""
    print("\n" + "="*60)
    print("7. FEATURE FLAGS")
    print("="*60)
    
    print(f"Offline Mode:     {'✅ Enabled' if settings.FEATURE_OFFLINE_MODE else '❌ Disabled'}")
    print(f"Dark Mode:        {'✅ Enabled' if settings.FEATURE_DARK_MODE else '❌ Disabled'}")
    print(f"Analytics:        {'✅ Enabled' if settings.FEATURE_ANALYTICS else '❌ Disabled'}")
    print(f"Notifications:    {'✅ Enabled' if settings.FEATURE_NOTIFICATIONS else '❌ Disabled'}")


def demo_usage_patterns():
    """Demo: Common usage patterns"""
    print("\n" + "="*60)
    print("8. COMMON USAGE PATTERNS")
    print("="*60)
    
    # Pattern 1: Check feature flag
    if settings.FEATURE_DARK_MODE:
        print("✅ Dark mode is enabled")
    
    # Pattern 2: Environment-specific behavior
    if settings.is_development():
        print("✅ Running in development mode - verbose logging enabled")
    
    # Pattern 3: Get with default
    page_size = settings.get('CUSTOM_PAGE_SIZE', settings.PERFORMANCE_PAGE_SIZE)
    print(f"✅ Page size: {page_size}")
    
    # Pattern 4: Conditional loading
    if settings.CACHE_ENABLED:
        print(f"✅ Cache enabled with TTL of {settings.CACHE_TTL}s")


def main():
    """Run all demos"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*15 + "CONFIGURATION SYSTEM DEMO" + " "*18 + "║")
    print("╚" + "="*58 + "╝")
    
    demo_basic_access()
    demo_all_config()
    demo_environment_detection()
    demo_categories()
    demo_runtime_changes()
    demo_helper_functions()
    demo_feature_flags()
    demo_usage_patterns()
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE")
    print("="*60)
    print("\nConfiguration loaded from:")
    print("  1. Default values")
    print("  2. config.ini (if exists)")
    print("  3. .env file (if exists)")
    print("  4. Environment variables")
    print("\nPriority: ENV_VARS > .env > config.ini > defaults")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
