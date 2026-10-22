import { useState } from 'react';
import { Button, Surface, TextField, Toggle } from '@xvadur/ui';
const materials = [{ id: 'flat', label: 'Plochý' }, { id: 'soft', label: 'Plastický' }, { id: 'neumorphic', label: 'Neumorphism' }];
export default function MaterialPreview() {
  const [material, setMaterial] = useState('neumorphic');
  return <div className="manual-material-example">
    <div className="manual-example-controls" role="group" aria-label="Porovnať materiály">{materials.map(item => <Button key={item.id} variant={item.id === material ? 'primary' : 'secondary'} aria-pressed={item.id === material} onClick={() => setMaterial(item.id)}>{item.label}</Button>)}</div>
    <div data-material={material}><Surface className="material-preview"><TextField label="Názov projektu" defaultValue="XVADUR" /><div className="example-row"><Button>Otvoriť projekt</Button><Button variant="secondary">Upraviť</Button><Toggle label="Zobraziť detail" /></div></Surface></div>
    <p className="manual-example-caption">Rovnaké prvky v troch materiáloch. Neumorfizmus je zvolený smer; intenzita a konkrétne použitie ešte zostávajú pracovné.</p>
  </div>;
}
