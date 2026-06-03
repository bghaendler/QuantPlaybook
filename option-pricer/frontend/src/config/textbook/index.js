import { BSM_DATA } from './BSM';
import { MERTON_DATA } from './Merton';
import { BLACK76_DATA } from './Black76'; // <--- This import must match the file above
import { ASAY_DATA } from './Asay';
import { GARMAN_DATA } from './Garman';
import { GEN_BSM_DATA } from './GenBSM';
import { BARRIER_STD_DATA } from './BarrierStd';
import { BRENNER_DATA } from './Brenner';
import { BLACK76F_DATA } from './Black76F';

export const TEXTBOOK_DATA = {
    bsm: BSM_DATA,
    merton: MERTON_DATA,
    black76: BLACK76_DATA, // <--- This export must match
    asay: ASAY_DATA,
    garman: GARMAN_DATA,
    gen_bsm: GEN_BSM_DATA,
    barrier_std: BARRIER_STD_DATA,
    brenner: BRENNER_DATA,
    black76f: BLACK76F_DATA
};