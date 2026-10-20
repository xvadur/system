import type { Ref } from 'react';

export type ActionVariant = 'primary' | 'secondary' | 'ghost' | 'danger';
export type ActionSize = 'sm' | 'md' | 'lg';
export type Tone = 'neutral' | 'success' | 'warning' | 'danger';

export function classes(...values: (string | undefined | false)[]): string {
  return values.filter(Boolean).join(' ');
}

export function assignRef<T>(ref: Ref<T> | undefined, value: T | null): void {
  if (typeof ref === 'function') ref(value);
  else if (ref) ref.current = value;
}
