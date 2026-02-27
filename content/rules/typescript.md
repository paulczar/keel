---
title: "TypeScript Standards"
description: "TypeScript and React coding conventions"
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
alwaysApply: false
tags: ["typescript", "react", "javascript"]
weight: 10
---

# TypeScript Standards

Standards for TypeScript and React development.

## Type Safety

- Enable `strict` mode in `tsconfig.json` — never disable it
- Avoid `any`; use `unknown` when the type is genuinely unknown, then narrow with type guards
- Prefer interfaces for object shapes; use type aliases for unions, intersections, and mapped types
- Use discriminated unions over optional fields for variant types
- Export types alongside their associated functions and components

## Naming Conventions

- **Variables and functions:** `camelCase`
- **Types and interfaces:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE` for true compile-time constants; `camelCase` for runtime values
- **Files:** `kebab-case.ts` for utilities, `PascalCase.tsx` for React components
- **Enums:** `PascalCase` name, `PascalCase` members

## React Components

- Use functional components with hooks — never class components
- Define props as an interface named `[ComponentName]Props`
- Destructure props in the function signature
- Keep components under 200 lines; extract sub-components when they grow
- Co-locate component, styles, types, and tests in the same directory
- Use `React.FC` sparingly — prefer explicit return types

```tsx
interface UserCardProps {
  user: User;
  onSelect: (id: string) => void;
}

export function UserCard({ user, onSelect }: UserCardProps) {
  return (
    <div onClick={() => onSelect(user.id)}>
      {user.name}
    </div>
  );
}
```

## State Management

- Keep state as local as possible — lift only when necessary
- Use `useState` for simple local state, `useReducer` for complex state logic
- Avoid prop drilling beyond 2 levels — use Context or a state manager
- Memoize expensive computations with `useMemo` and callbacks with `useCallback`
- Never store derived state — compute it during render

## Async Patterns

- Use `async`/`await` over raw Promises — never use `.then()` chains
- Always handle errors in async functions with try/catch
- Use `AbortController` for cancellable requests
- Type API responses explicitly — never trust `any` from `fetch` or Axios

## Imports

- Use named exports — avoid default exports (except for Next.js pages/layouts)
- Group imports: external libs → internal modules → relative imports → types
- Use path aliases (`@/`) for project-internal imports to avoid deep relative paths

## Testing

- Use Vitest or Jest with React Testing Library
- Test behavior, not implementation — query by role, label, or text
- Mock external dependencies at module boundaries, not internal functions
- Use `userEvent` over `fireEvent` for realistic user interaction simulation
