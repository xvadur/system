import { useId, useRef, useState, type ComponentPropsWithoutRef, type KeyboardEvent, type ReactNode } from 'react';
import { classes } from './shared.js';

export type TabItem = { id: string; label: ReactNode; content: ReactNode; disabled?: boolean };
export type TabsProps = Omit<ComponentPropsWithoutRef<'div'>, 'onChange'> & {
  label: string;
  items: readonly TabItem[];
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
};

/** Horizontal tabs with automatic activation and roving keyboard focus. IDs must be unique. */
export function Tabs({ label, items, value, defaultValue, onValueChange, className, ...props }: TabsProps) {
  const instanceId = useId();
  const [localValue, setLocalValue] = useState(defaultValue ?? items.find(item => !item.disabled)?.id);
  const buttonRefs = useRef(new Map<string, HTMLButtonElement>());
  const available = items.filter(item => !item.disabled);
  const requestedValue = value ?? localValue;
  const selectedId = available.some(item => item.id === requestedValue) ? requestedValue : available[0]?.id;
  const select = (id: string) => {
    if (value === undefined) setLocalValue(id);
    onValueChange?.(id);
  };
  const handleKey = (event: KeyboardEvent<HTMLButtonElement>, id: string) => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    const index = available.findIndex(item => item.id === id);
    const nextIndex = event.key === 'Home' ? 0 : event.key === 'End' ? available.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + available.length) % available.length;
    const next = available[nextIndex];
    if (next) {
      select(next.id);
      buttonRefs.current.get(next.id)?.focus();
    }
  };
  return <div {...props} className={classes('xv-tabs', className)}>
    <div className="xv-tabs__list" role="tablist" aria-label={label} aria-orientation="horizontal">
      {items.map(item => <button key={item.id} ref={node => { if (node) buttonRefs.current.set(item.id, node); else buttonRefs.current.delete(item.id); }} type="button" role="tab" id={`${instanceId}-tab-${item.id}`} aria-controls={`${instanceId}-panel-${item.id}`} aria-selected={selectedId === item.id} tabIndex={selectedId === item.id ? 0 : -1} disabled={item.disabled} className="xv-tabs__tab" onClick={() => select(item.id)} onKeyDown={event => handleKey(event, item.id)}>{item.label}</button>)}
    </div>
    {items.map(item => <div key={item.id} role="tabpanel" id={`${instanceId}-panel-${item.id}`} aria-labelledby={`${instanceId}-tab-${item.id}`} hidden={selectedId !== item.id} tabIndex={0} className="xv-tabs__panel">{item.content}</div>)}
  </div>;
}
