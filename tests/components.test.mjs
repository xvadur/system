import test from 'node:test';
import assert from 'node:assert/strict';
import { createElement as h } from 'react';
import { renderToStaticMarkup as render } from 'react-dom/server';
import { Button, ActionLink, TextField, TextArea, Toggle, Dialog, Tabs, ProjectCard, Notice, ThemeControl } from '../dist/index.js';

test('button stays a native button, avoids accidental submit, disables busy action', () => {
  const html = render(h(Button, { loading: true }, 'Uložiť'));
  assert.match(html, /type="button"/);
  assert.match(html, /disabled=""/);
  assert.match(html, /aria-busy="true"/);
  assert.match(html, /Uložiť/);
  assert.match(render(h(Button, { type: 'submit' }, 'Odoslať')), /type="submit"/);
});

test('navigation preserves native anchor behavior and safe new window relationship', () => {
  const html = render(h(ActionLink, { href: '/projekty/', target: '_blank' }, 'Projekty'));
  assert.match(html, /href="\/projekty\/"/);
  assert.match(html, /rel="noopener noreferrer"/);
  assert.doesNotMatch(html, /role="button"/);
});

test('field links visible label, description, existing hint and error by ID', () => {
  const html = render(h(TextField, { id: 'email', label: 'E-mail', description: 'Pomoc', error: 'Chyba', 'aria-describedby': 'external', required: true }));
  assert.match(html, /for="email"/);
  assert.match(html, /aria-describedby="external email-description email-error"/);
  assert.match(html, /aria-invalid="true"/);
  assert.match(html, /id="email-error"/);
  assert.match(html, /required=""/);
});

test('generated IDs remain unique for adjacent fields and textarea errors', () => {
  const html = render(h('div', null, h(TextField, { label: 'Prvé' }), h(TextField, { label: 'Druhé' }), h(TextArea, { label: 'Text', error: 'Doplň text' })));
  const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map(match => match[1]);
  assert.equal(ids.length, new Set(ids).size);
  assert.match(html, /<textarea[^>]+aria-invalid="true"/);
});

test('toggle has a native checkbox and a named touch label', () => {
  const html = render(h(Toggle, { id: 'detail', label: 'Detail', description: 'Vysvetlenie', defaultChecked: true }));
  assert.match(html, /type="checkbox"/);
  assert.match(html, /for="detail"/);
  assert.match(html, /aria-describedby="detail-description"/);
  assert.match(html, /checked=""/);
});

test('tabs expose one focusable selected tab and matching labelled panels', () => {
  const html = render(h(Tabs, { label: 'Projekt', defaultValue: 'second', items: [{ id: 'first', label: 'Prvá', content: 'A' }, { id: 'second', label: 'Druhá', content: 'B' }, { id: 'third', label: 'Tretia', content: 'C', disabled: true }] }));
  assert.equal((html.match(/aria-selected="true"/g) || []).length, 1);
  assert.equal((html.match(/tabindex="0"[^>]*class="xv-tabs__tab"/g) || []).length, 1);
  assert.match(html, /role="tablist" aria-label="Projekt"/);
  assert.equal((html.match(/role="tabpanel"/g) || []).length, 3);
  assert.equal((html.match(/ hidden=""/g) || []).length, 2);
});

test('dialog renders native semantics and is opened modally only after hydration', () => {
  const html = render(h(Dialog, { open: true, onOpenChange() {}, title: 'Potvrdenie', description: 'Vysvetlenie' }, 'Obsah'));
  assert.match(html, /^<dialog /);
  assert.match(html, /aria-labelledby="[^"]+-title"/);
  assert.match(html, /aria-describedby="[^"]+-description"/);
  assert.doesNotMatch(html, / open=""/);
  assert.match(html, /aria-label="Zavrieť"/);
});

test('project card displays caller content without fabricated facts', () => {
  const html = render(h(ProjectCard, { href: '/projekt/', title: 'Môj projekt', status: 'Vo vývoji' }));
  assert.match(html, /Môj projekt/);
  assert.match(html, /Vo vývoji/);
  assert.doesNotMatch(html, /users|používateľ|€|undefined/);
});

test('notices distinguish urgent error announcements and themes render without browser globals', () => {
  assert.match(render(h(Notice, { tone: 'danger' }, 'Chyba')), /role="alert"/);
  const theme = render(h(ThemeControl, { defaultValue: 'system' }));
  assert.equal((theme.match(/aria-pressed="true"/g) || []).length, 1);
  assert.match(theme, /Farebná téma/);
});
