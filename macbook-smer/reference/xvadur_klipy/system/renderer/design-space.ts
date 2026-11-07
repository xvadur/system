export type DesignSpace = {width:number;height:number};
type Values = Record<string,unknown>;
const record=(value:unknown):value is Values=>!!value&&typeof value==='object'&&!Array.isArray(value);

/** Only output-space fields are converted. Source crops and SceneSpec's own
 * coordinate system are deliberately never visited by this mapper. */
export function scaleOutputParameters(params:Values,output:DesignSpace,design?:DesignSpace,scene?:string):Values {
  if(!design||scene==='Authored')return params;
  const sx=output.width/design.width,sy=output.height/design.height;
  if(!Number.isFinite(sx)||!Number.isFinite(sy)||sx<=0||sy<=0)throw new Error('Invalid renderer design space');
  const box=(value:unknown)=>{
    if(!record(value))return value;
    return Object.fromEntries(Object.entries(value).map(([key,part])=>[key,typeof part==='number'&&Number.isFinite(part)&&['x','y','width','height'].includes(key)?part*(key==='x'||key==='width'?sx:sy):part]));
  };
  const framing=(value:unknown)=>{
    if(!record(value))return value;
    return {...value,...(value.viewport?{viewport:box(value.viewport)}:{}),...(Array.isArray(value.panels)?{panels:value.panels.map(panel=>record(panel)?{...panel,viewport:box(panel.viewport)}:panel)}:{})};
  };
  return {...params,
    ...(params.box?{box:box(params.box)}:{}),
    ...(params.highlight?{highlight:box(params.highlight)}:{}),
    ...(params.framing?{framing:framing(params.framing)}:{}),
    ...(Array.isArray(params.panels)?{panels:params.panels.map(panel=>record(panel)?{...panel,viewport:box(panel.viewport)}:panel)}:{}),
    ...(scene==='Diagram'&&Array.isArray(params.nodes)?{nodes:params.nodes.map(node=>record(node)?{...box(node) as Values,...(typeof node.fontSize==='number'?{fontSize:node.fontSize*sx}:{})}:node)}:{}),
    ...(typeof params.fontSize==='number'?{fontSize:params.fontSize*sx}:{})
  };
}
