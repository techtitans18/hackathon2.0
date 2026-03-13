# Development Guide

## Getting Started

### Setup Development Environment

1. **Install Python 3.9+**
```bash
python --version
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the App**
```bash
python main.py
```

## Project Architecture

### MVC Pattern
- **Models**: Data structures (models/)
- **Views**: UI screens (screens/ and kv/)
- **Controllers**: Business logic (services/)

### Key Components

#### Services Layer
- `APIClient`: Handles all HTTP requests
- `AuthService`: Manages authentication and tokens
- `EncryptionService`: Handles file encryption

#### Utils Layer
- `Validator`: Input validation
- `QRCodeUtil`: QR code generation
- `CacheManager`: Offline data caching

#### Screens Layer
- Each screen has .py (logic) and .kv (UI) files
- Screens organized by user role (patient, hospital, admin)

## Coding Standards

### Python Style Guide
- Follow PEP 8
- Use type hints where possible
- Maximum line length: 100 characters
- Use docstrings for functions

Example:
```python
def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, ""
    return False, "Invalid email format"
```

### KV File Guidelines
- Use consistent spacing (dp units)
- Group related widgets
- Use descriptive IDs
- Keep layouts simple

### Naming Conventions
- Classes: PascalCase (e.g., `PatientDashboardScreen`)
- Functions: snake_case (e.g., `load_records`)
- Constants: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)
- Private methods: _leading_underscore (e.g., `_get_headers`)

## Adding New Features

### 1. Create New Screen

**Step 1**: Create Python file
```python
# screens/patient/new_feature.py
from kivymd.uix.screen import MDScreen

class NewFeatureScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_enter(self):
        # Called when screen is displayed
        pass
```

**Step 2**: Create KV file
```kv
# kv/new_feature.kv
<NewFeatureScreen>:
    name: 'new_feature'
    
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "New Feature"
```

**Step 3**: Register in main.py
```python
from screens.patient.new_feature import NewFeatureScreen

# In build() method
sm.add_widget(NewFeatureScreen(name='new_feature'))
```

### 2. Add API Endpoint

```python
# In appropriate screen
response = self.api_client.get('/endpoint')
if 'error' in response:
    self.show_dialog("Error", response['error'])
    return

data = response.get('data')
# Process data
```

### 3. Add Validation

```python
# In utils/validators.py
@staticmethod
def validate_custom(value: str) -> Tuple[bool, str]:
    if condition:
        return True, ""
    return False, "Error message"
```

## Testing

### Manual Testing Checklist
- [ ] Login with all user roles
- [ ] Test offline functionality
- [ ] Test camera integration
- [ ] Test QR code generation
- [ ] Test API error handling
- [ ] Test form validation
- [ ] Test navigation between screens

### Device Testing
- Test on different screen sizes
- Test on Android and iOS
- Test with different Android versions
- Test with slow network

## Debugging

### Enable Debug Mode
```python
# config.py
DEBUG_MODE = True
```

### View Logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

1. **Import Errors**
   - Check __init__.py files
   - Verify module paths

2. **KV File Not Loading**
   - Check file name matches class name
   - Verify Builder.load_file() call

3. **API Connection Failed**
   - Check API_BASE_URL
   - Verify backend is running
   - Check network connectivity

## Performance Optimization

### Best Practices
- Use RecycleView for long lists
- Cache API responses
- Lazy load images
- Minimize widget tree depth
- Use Clock.schedule for heavy operations

### Memory Management
- Clear unused widgets
- Unload screens when not needed
- Limit cache size

## Security Best Practices

1. **Never hardcode credentials**
2. **Validate all user inputs**
3. **Use HTTPS in production**
4. **Encrypt sensitive data**
5. **Implement proper error handling**
6. **Keep dependencies updated**

## Git Workflow

1. Create feature branch
```bash
git checkout -b feature/new-feature
```

2. Make changes and commit
```bash
git add .
git commit -m "Add new feature"
```

3. Push and create PR
```bash
git push origin feature/new-feature
```

## Resources

- [Kivy Documentation](https://kivy.org/doc/stable/)
- [KivyMD Documentation](https://kivymd.readthedocs.io/)
- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [Python Style Guide](https://pep8.org/)
