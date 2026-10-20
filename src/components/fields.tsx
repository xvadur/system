import { useId, type ComponentPropsWithRef, type ReactNode } from 'react';
import { classes } from './shared.js';

type FieldContent = { label: ReactNode; description?: ReactNode; error?: ReactNode };

function describedBy(existing: string | undefined, descriptionId: string | undefined, errorId: string | undefined): string | undefined {
  return [existing, descriptionId, errorId].filter(Boolean).join(' ') || undefined;
}

export type TextFieldProps = Omit<ComponentPropsWithRef<'input'>, 'children'> & FieldContent;

export function TextField({ label, description, error, id, className, required, 'aria-describedby': externalDescription, 'aria-invalid': externalInvalid, ...props }: TextFieldProps) {
  const generatedId = useId();
  const fieldId = id ?? `xv-field-${generatedId}`;
  const descriptionId = description ? `${fieldId}-description` : undefined;
  const errorId = error ? `${fieldId}-error` : undefined;
  return <div className="xv-field">
    <label className="xv-field__label" htmlFor={fieldId}>{label}{required ? <span aria-hidden="true"> *</span> : null}</label>
    <input {...props} id={fieldId} required={required} aria-describedby={describedBy(externalDescription, descriptionId, errorId)} aria-invalid={error ? true : externalInvalid} className={classes('xv-input', className)} />
    {description ? <div id={descriptionId} className="xv-field__description">{description}</div> : null}
    {error ? <div id={errorId} className="xv-field__error">{error}</div> : null}
  </div>;
}

export type TextAreaProps = ComponentPropsWithRef<'textarea'> & FieldContent;

export function TextArea({ label, description, error, id, className, required, rows = 4, 'aria-describedby': externalDescription, 'aria-invalid': externalInvalid, ...props }: TextAreaProps) {
  const generatedId = useId();
  const fieldId = id ?? `xv-field-${generatedId}`;
  const descriptionId = description ? `${fieldId}-description` : undefined;
  const errorId = error ? `${fieldId}-error` : undefined;
  return <div className="xv-field">
    <label className="xv-field__label" htmlFor={fieldId}>{label}{required ? <span aria-hidden="true"> *</span> : null}</label>
    <textarea {...props} id={fieldId} rows={rows} required={required} aria-describedby={describedBy(externalDescription, descriptionId, errorId)} aria-invalid={error ? true : externalInvalid} className={classes('xv-input', 'xv-textarea', className)} />
    {description ? <div id={descriptionId} className="xv-field__description">{description}</div> : null}
    {error ? <div id={errorId} className="xv-field__error">{error}</div> : null}
  </div>;
}

export type ToggleProps = Omit<ComponentPropsWithRef<'input'>, 'type' | 'children'> & { label: ReactNode; description?: ReactNode };

export function Toggle({ label, description, id, className, 'aria-describedby': externalDescription, ...props }: ToggleProps) {
  const generatedId = useId();
  const inputId = id ?? `xv-toggle-${generatedId}`;
  const descriptionId = description ? `${inputId}-description` : undefined;
  return <div className="xv-toggle">
    <label className="xv-toggle__label" htmlFor={inputId}>
      <input {...props} type="checkbox" id={inputId} aria-describedby={describedBy(externalDescription, descriptionId, undefined)} className={classes('xv-toggle__input', className)} />
      <span className="xv-toggle__track" aria-hidden="true" /><span>{label}</span>
    </label>
    {description ? <div id={descriptionId} className="xv-toggle__description">{description}</div> : null}
  </div>;
}
