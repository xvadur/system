import type { ComponentPropsWithRef, ReactNode } from 'react';
import { classes, type ActionSize, type ActionVariant, type Tone } from './shared.js';

export type ButtonProps = ComponentPropsWithRef<'button'> & {
  variant?: ActionVariant;
  size?: ActionSize;
  /** The visible label stays in place while the action is busy. */
  loading?: boolean;
};

export function Button({ variant = 'primary', size = 'md', loading = false, disabled, className, children, type = 'button', ...props }: ButtonProps) {
  return <button {...props} type={type} disabled={disabled || loading} aria-busy={loading || undefined} className={classes('xv-button', className)} data-variant={variant} data-size={size}>
    {loading ? <span className="xv-spinner" aria-hidden="true" /> : null}{children}
  </button>;
}

export type ActionLinkProps = ComponentPropsWithRef<'a'> & { variant?: ActionVariant; size?: ActionSize; href: string };

export function ActionLink({ variant = 'secondary', size = 'md', className, children, rel, target, ...props }: ActionLinkProps) {
  return <a {...props} target={target} rel={rel ?? (target === '_blank' ? 'noopener noreferrer' : undefined)} className={classes('xv-button', className)} data-variant={variant} data-size={size}>{children}</a>;
}

export type BadgeProps = ComponentPropsWithRef<'span'> & { tone?: Tone };

export function Badge({ tone = 'neutral', className, ...props }: BadgeProps) {
  return <span {...props} className={classes('xv-badge', className)} data-tone={tone} />;
}

export type SurfaceProps = ComponentPropsWithRef<'div'>;

export function Surface({ className, ...props }: SurfaceProps) {
  return <div {...props} className={classes('xv-surface', className)} />;
}

export type ProjectCardProps = Omit<ComponentPropsWithRef<'a'>, 'title' | 'children'> & {
  href: string;
  title: string;
  description?: ReactNode;
  status?: ReactNode;
  image?: { src: string; alt: string; width?: number; height?: number };
  meta?: ReactNode;
};

export function ProjectCard({ title, description, status, image, meta, className, target, rel, ...props }: ProjectCardProps) {
  return <a {...props} target={target} rel={rel ?? (target === '_blank' ? 'noopener noreferrer' : undefined)} className={classes('xv-project-card', className)}>
    {image ? <img className="xv-project-card__image" src={image.src} alt={image.alt} width={image.width} height={image.height} loading="lazy" decoding="async" /> : null}
    <span className="xv-project-card__body">
      {status ? <span className="xv-project-card__status">{status}</span> : null}
      <span className="xv-project-card__title">{title}<span aria-hidden="true">↗</span></span>
      {description ? <span className="xv-project-card__description">{description}</span> : null}
      {meta ? <span className="xv-project-card__meta">{meta}</span> : null}
    </span>
  </a>;
}

export type NoticeProps = Omit<ComponentPropsWithRef<'div'>, 'title'> & { tone?: Tone; title?: ReactNode };

export function Notice({ tone = 'neutral', title, children, className, role, ...props }: NoticeProps) {
  return <div {...props} role={role ?? (tone === 'danger' ? 'alert' : 'status')} className={classes('xv-notice', className)} data-tone={tone}>
    {title ? <p className="xv-notice__title">{title}</p> : null}
    <div className="xv-notice__content">{children}</div>
  </div>;
}

export type EmptyStateProps = Omit<ComponentPropsWithRef<'div'>, 'title' | 'children'> & { title: ReactNode; description?: ReactNode; action?: ReactNode };

export function EmptyState({ title, description, action, className, ...props }: EmptyStateProps) {
  return <div {...props} className={classes('xv-empty-state', className)}>
    <p className="xv-empty-state__title">{title}</p>
    {description ? <div className="xv-empty-state__description">{description}</div> : null}
    {action ? <div className="xv-empty-state__action">{action}</div> : null}
  </div>;
}

export type AccordionProps = Omit<ComponentPropsWithRef<'details'>, 'title'> & { title: ReactNode };

export function Accordion({ title, children, className, ...props }: AccordionProps) {
  return <details {...props} className={classes('xv-accordion', className)}>
    <summary className="xv-accordion__summary">{title}<span className="xv-accordion__indicator" aria-hidden="true">+</span></summary>
    <div className="xv-accordion__content">{children}</div>
  </details>;
}
