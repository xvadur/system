import { useEffect, useId, useRef, type ComponentPropsWithRef, type MouseEvent, type ReactNode } from 'react';
import { assignRef, classes } from './shared.js';

export type DialogProps = Omit<ComponentPropsWithRef<'dialog'>, 'open' | 'title' | 'children'> & {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: ReactNode;
  description?: ReactNode;
  children: ReactNode;
  closeLabel?: string;
  dismissOnBackdrop?: boolean;
};

/** Uses the browser's modal focus containment; hydrate the owning React island in Astro. */
export function Dialog({ open, onOpenChange, title, description, children, closeLabel = 'Zavrieť', dismissOnBackdrop = true, className, ref, onCancel, onClose, onClick, ...props }: DialogProps) {
  const instanceId = useId();
  const dialogRef = useRef<HTMLDialogElement>(null);
  const openerRef = useRef<HTMLElement | null>(null);
  const restoreFocus = () => {
    if (openerRef.current?.isConnected) openerRef.current.focus();
    openerRef.current = null;
  };
  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (open && !dialog.open) {
      openerRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null;
      dialog.showModal();
    } else if (!open && dialog.open) {
      dialog.close();
      restoreFocus();
    }
  }, [open]);
  useEffect(() => () => {
    dialogRef.current?.close();
    restoreFocus();
  }, []);
  const handleBackdrop = (event: MouseEvent<HTMLDialogElement>) => {
    onClick?.(event);
    if (event.defaultPrevented || !dismissOnBackdrop || event.target !== event.currentTarget) return;
    const rect = event.currentTarget.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) onOpenChange(false);
  };
  return <dialog {...props} ref={node => { dialogRef.current = node; assignRef(ref, node); }} aria-labelledby={`${instanceId}-title`} aria-describedby={description ? `${instanceId}-description` : props['aria-describedby']} className={classes('xv-dialog', className)} onClick={handleBackdrop} onCancel={event => {
    onCancel?.(event);
    if (!event.defaultPrevented) { event.preventDefault(); onOpenChange(false); }
  }} onClose={event => {
    onClose?.(event);
    restoreFocus();
    if (open) onOpenChange(false);
  }}>
    <header className="xv-dialog__header">
      <h2 className="xv-dialog__title" id={`${instanceId}-title`}>{title}</h2>
      <button type="button" className="xv-dialog__close" aria-label={closeLabel} onClick={() => onOpenChange(false)}><span aria-hidden="true">×</span></button>
    </header>
    {description ? <div className="xv-dialog__description" id={`${instanceId}-description`}>{description}</div> : null}
    <div className="xv-dialog__content">{children}</div>
  </dialog>;
}
