import { Button, makeStyles } from '@material-ui/core';
import { observer } from 'mobx-react';
import { FC } from 'react';

import translate from '../../utils/transform';

const useStyles = makeStyles({
  root: {
    display: 'flex',
  },
});

type Props = {
  disabled?: boolean;
  label: string;
  path: string | null;
};

const Symbol: FC<Props> = ({ disabled = false, path, label }) => {
  const styles = useStyles();

  return (
    <div className={styles.root}>
      <Button
        disabled={disabled}
        startIcon={
          <svg height="25" viewBox="0 0 25 25" width="25">
            {path && <path d={path} opacity="0.5" transform={translate(25 / 2)} />}
          </svg>
        }
      >
        {label}
      </Button>
    </div>
  );
};

export default observer(Symbol);
