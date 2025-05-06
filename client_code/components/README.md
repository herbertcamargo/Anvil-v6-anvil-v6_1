# React and Vue Components for Anvil

This directory contains React and Vue components that can be used in your Anvil application.

## Setup

1. Install Node.js and npm if you haven't already.
2. Navigate to this directory (`client_code/components`) in your terminal.
3. Run the build script:
   ```
   # On Windows
   ./build.ps1
   
   # On Mac/Linux
   chmod +x build.sh
   ./build.sh
   ```

## Adding New Components

### React Components

1. Create your component file in `src/react/` directory.
2. Export your component.
3. Add it to the components object in `src/react/index.js`.

Example:

```javascript
// src/react/MyNewComponent.js
import React from 'react';

const MyNewComponent = ({ title }) => {
  return <div>{title}</div>;
};

export default MyNewComponent;
```

Then in `src/react/index.js`:

```javascript
import MyNewComponent from './MyNewComponent';

// ...

const components = {
  TodoList: TodoList,
  MyNewComponent: MyNewComponent
};
```

### Vue Components

1. Create your component file in `src/vue/` directory.
2. Export your component.
3. Add it to the components object in `src/vue/index.js`.

Example:

```javascript
// src/vue/MyNewComponent.vue
<template>
  <div>{{ title }}</div>
</template>

<script>
export default {
  name: 'MyNewComponent',
  props: ['title']
};
</script>
```

Then in `src/vue/index.js`:

```javascript
import MyNewComponent from './MyNewComponent.vue';

// ...

const components = {
  TodoList: TodoList,
  MyNewComponent: MyNewComponent
};
```

## Using Components in Anvil Forms

1. Add an HTML component to your form with an ID:
   ```html
   <div id="my-component-container"></div>
   ```

2. In your form's Python code, render the component:
   ```python
   import anvil.js
   
   # For React
   anvil.js.call_js('window.renderReactComponent', 'MyNewComponent', 'my-component-container', {'title': 'Hello World'})
   
   # For Vue
   anvil.js.call_js('window.renderVueComponent', 'MyNewComponent', 'my-component-container', {'title': 'Hello World'})
   ```

## Building after Changes

After making changes to your components, run the build script again to rebuild and deploy them. 