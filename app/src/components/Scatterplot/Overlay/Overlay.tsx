import { ScaleLinear } from 'd3';
import { observer } from 'mobx-react';
import React, { FC } from 'react';

import { DBScanInfo, KMeansInfo, Prediction } from '../../../Store/Types/Prediction';

import DBScan from './DBScan';
import KMeans from './KMeans';

type Props = {
  prediction: Prediction;
  xScale: ScaleLinear<number, number>;
  yScale: ScaleLinear<number, number>;
};

const Overlay: FC<Props> = ({ prediction, xScale, yScale }: Props) => {
  const { info } = prediction;

  switch (prediction.algorithm) {
    case 'DBScan':
      switch (prediction.intent) {
        case 'Cluster':
          return <DBScan info={info as DBScanInfo} xScale={xScale} yScale={yScale} />;
        default:
          break;
      }
      break;
    case 'KMeans':
      return <KMeans info={info as KMeansInfo} xScale={xScale} yScale={yScale} />;
    default:
      break;
  }

  return <></>;
};

export default observer(Overlay);
