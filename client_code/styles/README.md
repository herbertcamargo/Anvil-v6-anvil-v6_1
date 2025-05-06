# SASS Styling System for Anvil

This directory contains a SASS-based styling system for the Anvil application. SASS provides more maintainable styling with variables, mixins, nesting, and other advanced features.

## Project Structure

- `sass/` - SASS source files
  - `_variables.scss` - Global variables for colors, typography, spacing, etc.
  - `_mixins.scss` - Reusable mixins for common styles
  - `components/` - Component-specific styles
    - `_todo.scss` - Styles for Todo component
    - `_video-processor.scss` - Styles for Video Processor component
    - `_buttons.scss` - Common button styles
    - `_forms.scss` - Form element styles
    - `_layout.scss` - Layout utilities
  - `main.scss` - Main SASS file that imports all others
- `css/` - Compiled CSS files (output)
- `scripts/` - Helper scripts
  - `copy-to-theme.js` - Copies compiled CSS to the theme directory

## Getting Started

### Prerequisites

To build the SASS files, you'll need:

1. [Node.js and npm](https://nodejs.org/) - for the build tools

### Building

Run the build script to compile SASS to CSS and copy the files to the theme directory:

```bash
# On Windows
./build.ps1

# On Mac/Linux
chmod +x build.sh
./build.sh
```

### Development

During development, you can use the watch mode to automatically recompile SASS files when they change:

```bash
cd client_code/styles
npm run watch
```

## Usage

### Including Styles in Anvil Forms

After building the styles, they will be available in the `theme/css` directory. To use them in your Anvil forms, add a link to the CSS file:

```python
from anvil import *
import anvil.js
from anvil.js.window import document

class MyForm(Form):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    # Add link to the main CSS file
    head = document.getElementsByTagName('head')[0]
    link = document.createElement('link')
    link.rel = 'stylesheet'
    link.type = 'text/css'
    link.href = '_/theme/css/main.css'
    head.appendChild(link)
```

### Using Variables and Mixins

The styling system defines variables and mixins for consistent design:

#### Variables

```scss
// Colors
$primary-color: #4CAF50;
$secondary-color: #2196F3;

// Typography
$font-family-base: Arial, sans-serif;
$font-size-base: 16px;

// Spacing
$spacing-medium: 16px;
```

#### Mixins

```scss
// Button mixin
@include button-primary;

// Responsive mixin
@include mobile {
  // Styles for mobile devices
}

// Container mixin
@include container;
```

## Customization

To customize the styling:

1. Edit the variables in `sass/_variables.scss` to change global design tokens
2. Modify component styles in the respective SASS files
3. Add new components by creating new files in `sass/components/` and importing them in `main.scss`
4. Run the build script to apply changes

## Best Practices

1. Use variables for consistent design values
2. Create mixins for reusable style patterns
3. Nest selectors to maintain hierarchy
4. Keep component styles separate
5. Use meaningful class names that follow a consistent pattern 