# Address Mapping Web App

## Overview

This web application is a modern, scalable, and extensible SvelteKit project for calculating the distance between two addresses and viewing the user's historical queries. It demonstrates best practices in component-driven development, UI/UX design, and API integration.

---

## Pages

### 1. Distance Calculation (`/`)

- **Purpose:** Allows users to input two addresses and calculate the distance between them.
- **Features:**
  - Input fields for source and destination addresses.
  - Radio buttons to select the unit (miles, kilometers, or both).
  - A calculate button that triggers a POST API call and displays the result.
  - Validation ensures both addresses are filled before enabling calculation.
  - Displays the calculated distance in the selected unit(s).

### 2. Historical Queries (`/history`)

- **Purpose:** Displays a table of all previous distance queries made by the user.
- **Features:**
  - Fetches data from a GET API endpoint.
  - Renders a responsive, scrollable table with source, destination, and distances.
  - Handles loading and error states gracefully.

---

## Component Workflow & Extensibility

The app is built with a set of **reusable, composable components**:

- **Button:**
  - Supports variants (primary, secondary, etc.), icons, and all native button props.
  - Used for all actions, ensuring consistent look and feel.
- **Input:**
  - Reusable for any text input with dynamic label, placeholder, and validation.
- **RadioButton:**
  - Used for unit selection, but can be reused for any radio group in the app.
- **Card:**
  - Provides a consistent, modern container for grouping content.
- **Table:**
  - Accepts dynamic headers and data, with built-in ellipsis and tooltips for overflow.
  - Can be extended for sorting, pagination, or row actions.
- **PageLayout:**
  - Shared layout for all pages, with dynamic title/subtitle and slot for content.

**Extending the App:**

- New features or pages can be built by composing these components.
- The design system is consistent and easy to maintain.
- Adding new input types, buttons, or tables is straightforward.

---

## Tailwind CSS & Theming

- **Utility-First:** Tailwind is used for all styling, enabling rapid prototyping and consistent design.
- **Theme Customization:**
  - Custom colors, font, and spacing are defined in the Tailwind config and `app.css`.
  - The global font is Inter, and the color palette is set for backgrounds, cards, and text.
- **Responsive Design:**
  - Utility classes like `md:flex-row` and `w-full` ensure the app looks great on all devices.

---

## Validation & User Experience

- The **Calculate** button is only enabled when both address fields are filled, preventing invalid API calls.
- Loading and error states are clearly communicated to the user (e.g., disabled button, toast notifications).
- The app provides instant feedback and clear error handling for a smooth user experience.

---

## Core Functionality

- **Distance Calculation:**
  - Users can calculate the distance between any two places in the world.
  - Results are shown in kilometers, miles, or both, depending on user selection.
  - The calculation is powered by a backend API, ensuring accuracy and scalability.
- **History:**
  - All previous queries are available in a sortable, readable table.
  - Each entry shows both addresses and the calculated distances.

---

## Development Thought Process & Workflow

- **Component-Driven:**
  - The app was designed with reusability and scalability in mind.
  - Each UI element is a standalone component, making the codebase easy to extend and maintain.
- **Best Practices:**
  - TypeScript interfaces for API requests and responses ensure type safety.
  - All API calls are handled with proper error management and user feedback.
  - Accessibility is considered in all components (labels, focus states, tooltips).
- **Rapid Iteration:**
  - Tailwind's utility classes enabled fast prototyping and consistent design.
  - Theming and layout are centralized for easy updates.
- **Extensibility:**
  - The architecture allows for easy addition of new features (e.g., authentication, more analytics, export options).

---

## How to Extend

- Add new pages by composing existing components.
- Extend the Table for features like sorting or pagination.
- Add new input types or validation rules as needed.
- Update the theme in `app.css` and Tailwind config for branding.

---

## Summary

This app is a foundation for robust, scalable, and beautiful web applications. It demonstrates how thoughtful component design, utility-first CSS, and best practices in SvelteKit can deliver a great user and developer experience.

```bash
# create a new project in the current directory
npx sv create

# create a new project in my-app
npx sv create my-app
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.
