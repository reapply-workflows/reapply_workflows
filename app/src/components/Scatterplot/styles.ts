import { makeStyles } from '@material-ui/core';

import { IPNS, ISNP, MATCHES, NON_UNION, UNION } from '../ColorSpecs';

const useScatterplotStyle = makeStyles({
  newMark: { stroke: 'blue', strokeWidth: '1', fill: 'blue !important' },
  removedMark: {
    stroke: 'red',
    strokeWidth: '3',
    strokeLinecap: 'round',
  },
  movedLine: {
    opacity: '0.5',
    stroke: 'blue',
    fill: 'blue !important',
    strokeWidth: '1',
    strokeLinecap: 'round',
  },
  movedPoint: {
    fill: 'black',
  },
  regularMark: {
    fill: 'black',
  },
  nonUnionMark: {
    fill: NON_UNION,
  },
  unionMark: {
    fill: UNION,
    stroke: UNION,
  },
  regularForceMark: {
    fill: 'black !important',
    opacity: 0.2,
  },
  intermittentHighlight: {
    fill: 'red',
  },
  matches: {
    fill: `${MATCHES} !important`,
    opacity: 1,
  },
  isnp: {
    fill: `${ISNP} !important`,
    opacity: 1,
  },
  ipns: {
    fill: `${IPNS} !important`,
    opacity: 1,
  },
});

export default useScatterplotStyle;
