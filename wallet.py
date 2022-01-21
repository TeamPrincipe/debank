# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 14:42:25 2021

@author: simosc
"""

from typing import Dict, Optional
import requests
import json
import hmac
import hashlib
import time
import datetime


class Wallet :
    
    API_URL = "https://openapi.debank.com" 
    
    # api version
    V1 = '/v1'
    
    # path
    CHAIN = '/chain'
    CHAIN_BALANCE = '/chain_balance'
    COMPLEX_PROTOCOL_LIST = '/complex_protocol_list'
    LIST = '/list'
    LIST_BY_IDS = '/list_by_ids'
    PROTOCOL = '/protocol'
    SIMPLE_PROTOCOL_LIST = '/simple_protocol_list'
    TOKEN = '/token'
    TOKEN_LIST = '/token_list'
    TOKEN_SEARCH = '/token_search'
    TOTAL_BALANCE = '/total_balance'
    USER = '/user'
    
    # request api
    ID = '?id='
    CHAIN_ID = '?chain_id='
    
    # other requirements
    ADDRESS = '&id='
    AND_CHAIN = '&chain_id='
    HAS_BALANCE = '&has_balance='
    IDS = '&ids='
    IS_ALL = '&is_all='
    PROTOCOL_ID = '&protocol_id='
    Q = '&q='
    TOKEN_ID = '&token_id='
    
    # optional GET condition
    OPTION_REQ = 'application/json'
    ALL_PROTOCOL = ['bsc_bdollar', 'bsc_bvault', 'bsc_beefy', 'bsc_beglobal', 'bsc_dsgmetaverse', 'bsc_fletaconnect', 'bsc_pancakeswap', 'bsc_arenaswap', 
                    'bsc_bakeryswap', 'bsc_barnbridge', 'bsc_knightswap', 'bsc_kebab', 'bsc_singular', 'bsc_thoreum', 'bsc_timewarp', 'bsc_hunnydao', 
                    'bsc_orion', 'bsc_venus', 'bsc_feeder', 'bsc_goose', 'bsc_depth', 'bsc_growing', 'bsc_helmet', 'bsc_1inch', 'bsc_revault', 
                    'bsc_leonicornswap', 'bsc_ten', 'bsc_elk', 'bsc_cream', 'bsc_trustpad', 'bsc_positionex', 'bsc_autofarm', 'bsc_xswap', 
                    'bsc_pancakebunny', 'bsc_alpacafinance', 'bsc_rabbitfinance', 'bsc_qian', 'bsc_bscstation', 'bsc_acryptos', 'bsc_acsi', 
                    'bsc_alpha', 'bsc_dodoex', 'bsc_ellipsis', 'bsc_julswap', 'bsc_pureswap', 'bsc_belt', 'bsc_smoothy', 'bsc_squidstake', 
                    'bsc_nerve', 'bsc_mdex', 'bsc_klend', 'bsc_yfv', 'bsc_forbank', 'bsc_badger', 'bsc_cyclone', 'bsc_apeswap', 'bsc_twindex', 
                    'bsc_swapking', 'bsc_marshmallowdefi', 'bsc_wardenswap', 'bsc_wault', 'bsc_dopple', 'bsc_sakeswap', 'bsc_deerfi', 'bsc_polkastarter', 
                    'bsc_fluity', 'bsc_coinwind', 'bsc_panther', 'bsc_stakedao', 'bsc_horizon', 'bsc_bzx2', 'bsc_privacyswap', 'bsc_solo', 'bsc_kalata', 
                    'bsc_flux', 'bsc_wepiggy', 'bsc_dforcelending', 'bsc_kokomoswap', 'bsc_bomb', 'bsc_iron', 'bsc_yfii', 'bsc_biswap', 'bsc_babyswap', 
                    'bsc_impossible', 'bsc_eleven', 'bsc_pandaswap', 'bsc_latteswap', 'bsc_jetswap', 'bsc_hyfi', 'bsc_steak_bank', 'bsc_swamp', 
                    'bsc_treedefi', 'bsc_fortress', 'bsc_blizzard', 'bsc_chemix', 'bsc_pancakehunny', 'bsc_coinswap', 'bsc_coinswap_dex', 'bsc_definix', 
                    'bsc_aperocket', 'bsc_aperocket_v2', 'bsc_cafeswap', 'bsc_kalmar', 'bsc_bunicorn', 'bsc_cubdefi', 'bsc_harvest', 'bsc_tranchess', 
                    'bsc_openocean', 'bsc_bxh', 'bsc_golff', 'bsc_dmm_exchange', 'bsc_piggy', 'bsc_cashcow', 'bsc_pinecone', 'bsc_alita', 'bsc_burgerswap', 
                    'bsc_qbt', 'bsc_bunnypark', 'bsc_popsicle', 'bsc_dyp', 'bsc_honeyfarm', 'bsc_moonpot', 'bsc_bifi', 'bsc_zoo', 'bsc_channels', 
                    'bsc_gambit', 'bsc_thegrandbanks', 'bsc_synapse', 'bsc_farmhero', 'bsc_scientix', 'bsc_marsecosystem', 'bsc_hyperjump', 'bsc_annex', 
                    'bsc_planetfinance', 'bsc_insurace', 'bsc_macaronswap', 'bsc_yieldparrot', 'bsc_mcdex', 'bsc_pacoca', 'bsc_autoshark', 'bsc_wasabix', 
                    'bsc_gibxswap', 'bsc_seeder', 'bsc_sil', 'bsc_ysl', 'bsc_mushrooms', 'bsc_gyro', 'bsc_atlantis', 'bsc_ocp', 'bsc_babycake', 
                    'bsc_taichidao', 'bsc_bagels', 'bsc_mound', 'bsc_lendhub', 'bsc_bsc33', 'bsc_pidao', 'bsc_wheat', 'bsc_sheepdex', 'bsc_alturanft', 
                    'bsc_metaversepro', 'bsc_jadeprotocol', 'bsc_planetfinance_lending', 'bsc_legendfantasywar', 'bsc_seedify', 'bsc_ola_apeswap', 
                    'bsc_ouro', 'bsc_stonedefi', 'bsc_nemesisdao', 'bsc_linear', 'bsc_rabbit_dao', 'bsc_jswap', 'bsc_deri', 'bsc_chargedefi', 'bsc_unusdao', 
                    'bsc_parsiq', 'bsc_sheeshafinance', 'bsc_elfinkingdom', 'bsc_woo', 'bsc_killswitch', 'bsc_stackos', 'bsc_galaxygoggle', 'bsc_yieldwolf', 
                    'bsc_dibsmoney', 'bsc_themanor', 'bsc_wisteriaswap', 'bsc_moonstarter', 'bsc_lightning', 'bsc_spintop', 'bsc_eulertools', 
                    'bsc_singularitydao', 'bsc_chromia', 'bsc_binaryx', 'eth2', 'aladdin', 'alpha', 'alpha2', 'alchemix', 'ankr', 'sunrisegaming', 
                    'everipedia', 'timewarp', 'uniswap2', 'uniswap3', 'compound', 'fiatdao', 'enterdao', 'lyra', 'curve', 'pendle', 'makerdao', 'tempus', 
                    'cream', 'stakeborg', 'rocketpool', 'elk', 'ethix', 'orion', 'bumper', 'polkastarter', 'badger', 'yearn2', 'yearn3', 'harvest', 'idle', 
                    'iearn', 'liqee', 'mars', 'kyber', 'aave2', '1inch2', 'apwine', 'synthetix', 'reflexer', 'vesper', 'pooltogether', 'barnbridge', 'uma', 
                    'pods', 'floatprotocol', 'sushiswap', 'saddle', 'aave', 'balancer', 'bancor', 'frax', 'nexus', 'cream2', 'dydx', 'keeperdao', 'yfdai', 
                    'tokenlon', 'bdp', 'boringdao', 'derivadex', 'dodoex', 'index', 'defiswap', 'uniswap', 'apy', 'stakedao', 'qian', 'corevault', 
                    'aave_amm', 'mstable', 'xtoken', 'mirror', 'smoothy', 'fei', 'dmm_exchange', 'truefi', 'dego', 'hegic', 'ribbon', 'tokensets', 'shell', 
                    'liquity', 'forbank2', 'unit', 'cover', 'opyn', 'opyn2', 'mooniswap', 'basiscash', 'powerpool', 'piedao', 'defidollar', 'perpetual', 
                    'yfii', 'yaxis', 'acbtc', 'bzx2', 'wepiggy', 'bprotocol', 'component', 'swerve', 'kine', 'rari', 'yieldprotocol', 'armor', 'balancer2', 
                    'integral', 'sakeswap', 'ruler', 'enzyme', 'convex', 'unipilot', 'pickle', 'lido', 'dforcelending', 'xsigma', 'bella', 'cofix', 
                    'olympusdao', 'olympusdao_pro', '0x', 'shibaswap', 'abracadabra', 'nft20', 'bao', 'shapeshift', 'cardstarter', 'sushiswap_lending', 
                    'inverse', 'illuvium', 'indexed', 'stakewise', 'instadapp', 'thegraph', 'mimo', '88mph2', 'onx', 'openocean', 'golff', 'stacker', 
                    'tokemak', 'volmex', 'alpha_tokenomics', 'naos', 'cvi', 'lixir', 'universexyz', 'popsicle', 'element', 'dhedge', 'nftx', 'dyp', 
                    'linkpool', 'ondo', 'gro', 'unfederalreserve', 'bifi', 'impermax', 'deversifi', 'synapse', 'mushrooms', 'betafinance', 'crucible', 
                    'bridgemutual', 'leaguedao', 'insurace', 'dfx', 'akropolis', 'cryptex', 'wasabix', 'mark', 'clipper', 'poptown', 'maple', 'fodl', 
                    'visor', 'sil', 'cook', 'rally', 'basket', 'universefinance', 'klondike', 'temple', 'charmfi', 'alkemi', 'yam', 'squid', 
                    'polygon_staking', 'snowswap', 'meritcircle', 'chfry', 'angle', 'plaza', 'unagii', 'umb', 'across', 'monox', 'stackos', 'paraswap', 
                    'duckdao', 'dogsofelon', 'saffron', 'lobis', 'ousd', 'bent', 'cerberusdao', 'syntropynet', 'stonedefi', 'bobagateway', 'fixedforex', 
                    'notional', 'paladin', 'edennetwork', 'redactedcartel', 'sheeshafinance', 'strongblock', 'vader', 'superfarm', 'manifest', 'neworder', 
                    'sipherxyz', 'euler', '0xmons', 'theopendao', 'daoofdiamonds', 'looksrare', 'sandbox', 'vlaunch', 'wilderworld', 'vaultinc', 'feeswtf', 
                    'atlasusv', 'izumi', 'api3', 'singularitydao', 'fujidao', 'rainmaker', 'heco_beefy', 'heco_booster', 'heco_mdex', 'heco_depth', 
                    'heco_lendhub', 'heco_bxh', 'heco_coinwind', 'heco_filda', 'heco_solo', 'heco_pippi', 'heco_pilot', 'heco_channels', 'heco_belt', 
                    'heco_makiswap', 'heco_dogeswap', 'heco_hogt', 'heco_hfione', 'heco_back', 'heco_wepiggy', 'heco_yfii', 'heco_elk', 'heco_cocoswap', 
                    'heco_golff', 'heco_autofarm', 'heco_flux', 'heco_newland', 'heco_hswap', 'heco_demeter', 'xdai_honeyswap', 'xdai_bao', 
                    'xdai_component', 'xdai_hop', 'xdai_curve', 'xdai_agave', 'xdai_elk', 'xdai_sushiswap', 'xdai_swapr', 'xdai_symmetric', 
                    'xdai_superfluid', 'matic_aave', 'matic_quickswap', 'matic_comethswap', 'matic_polyroll', 'matic_hop', 'matic_dfyn', 'matic_curve', 
                    'matic_smartswap', 'matic_mstable', 'matic_pollyfinance', 'matic_sushiswap', 'matic_singular', 'matic_polywhale', 'matic_pooltogether', 
                    'matic_bzx2', 'matic_beefy', 'matic_dodoex', 'matic_entropyfi', 'matic_pancakebunny', 'matic_polycake', 'matic_polycat', 'matic_elk', 
                    'matic_mai', 'matic_iron', 'matic_adamant', 'matic_sxc', 'matic_wault', 'matic_apeswap', 'matic_balancer2', 'matic_dmm_exchange', 
                    'matic_wepiggy', 'matic_firebird', 'matic_jetswap', 'matic_cream', 'matic_cafeswap', 'matic_solo', 'matic_iron2', 'matic_polycrystal', 
                    'matic_dinoswap', 'matic_stakedao', 'matic_polypup', 'matic_swamp', 'matic_harvest', 'matic_augury', 'matic_sushiswap_lending', 
                    'matic_iron2_lending', 'matic_pickle', 'matic_pearzap', 'matic_fortube', 'matic_volmex', 'matic_autofarm', 'matic_instadapp', 
                    'matic_dhedge', 'matic_eleven', 'matic_impermax', 'matic_synapse', 'matic_farmhero', 'matic_insurace', 'matic_gravityfinance', 
                    'matic_wasabix', 'matic_beluga', 'matic_klimadao', 'matic_mushrooms', 'matic_kogefarm', 'matic_kittyfinance', 'matic_dfx', 
                    'matic_apwine', 'matic_badger', 'matic_barnbridge', 'matic_flux', 'matic_snowswap', 'matic_otterclam', 'matic_relaychain', 
                    'matic_market', 'matic_monox', 'matic_yieldwolf', 'matic_superfluid', 'matic_thegrandbanks', 'matic_stonedefi', 'matic_idex3', 
                    'matic_tesr', 'matic_mimo', 'matic_jarvis', 'matic_idle', 'matic_sheeshafinance', 'matic_vesper', 'matic_uniswap3', 'matic_tokensets', 
                    'matic_tetu', 'matic_nidhidao', 'matic_nachoxyz', 'matic_angle', 'matic_popsicle', 'matic_cryptoraiders', 'matic_vesq', 'matic_parsiq', 
                    'matic_sandbox', 'matic_prxyfi', 'matic_gainsnetwork', 'matic_atlasusv', 'matic_izumi', 'matic_aavegotchi', 'matic_cubo', 
                    'ftm_pwawallet', 'ftm_beefy', 'ftm_curve', 'ftm_cream', 'ftm_liquiddriver', 'ftm_popsicle', 'ftm_spiritswap', 'ftm_yearn2', 
                    'ftm_olive', 'ftm_feeder', 'ftm_dmm_exchange', 'ftm_spookyswap', 'ftm_sushiswap', 'ftm_scarecrow', 'ftm_beluga', 'ftm_hundred', 
                    'ftm_fantompup', 'ftm_raven', 'ftm_shade', 'ftm_scarab', 'ftm_trickortreat', 'ftm_bouje', 'ftm_dfyn', 'ftm_waka', 'ftm_ester', 
                    'ftm_autofarm', 'ftm_scream', 'ftm_morpheusswap', 'ftm_liquity', 'ftm_swamp', 'ftm_elk', 'ftm_tarot', 'ftm_reaper', 'ftm_grim', 
                    'ftm_singular', 'ftm_olympusdao_pro', 'ftm_eleven', 'ftm_iron2', 'ftm_paintswap', 'ftm_jetswap', 'ftm_abracadabra', 'ftm_stakesteak', 
                    'ftm_geist', 'ftm_beethovenx', 'ftm_synapse', 'ftm_robovault', 'ftm_soul', 'ftm_pearzap', 'ftm_tomb', 'ftm_meso', 'ftm_zoodex', 
                    'ftm_mai', 'ftm_mushrooms', 'ftm_kogefarm', 'ftm_shibafantom', 'ftm_exodia', 'ftm_coffin', 'ftm_spartacus', 'ftm_fantohm', 
                    'ftm_hectordao', 'ftm_trava', 'ftm_yieldwolf', 'ftm_ola_spiritswap', 'ftm_gizadao', 'ftm_spartacadabra', 'ftm_summitdefi', 
                    'ftm_paprprintr', 'ftm_knightswap', 'ftm_market', 'ftm_revenant', 'ftm_vedao', 'ftm_2omb', 'ftm_fujidao', 'ftm_protofi', 
                    'okt_aiswap', 'okt_wepiggy', 'okt_flux', 'okt_sushiswap', 'okt_kswap', 'okt_fortube', 'okt_sakeswap', 'okt_cherryswap', 
                    'okt_acmd', 'okt_pandaswap', 'okt_solo', 'okt_cocoswap', 'okt_bxh', 'okt_klend', 'okt_jswap', 'okt_eleven', 'okt_farmhero', 
                    'okt_ofi', 'okt_sil', 'okt_cook', 'okt_elk', 'okt_lendhub', 'okt_pickle', 'okt_islandswap', 'avax_axial', 'avax_beefy', 'avax_benqi', 
                    'avax_baguette', 'avax_complus', 'avax_traderjoexyz', 'avax_pangolin', 'avax_lydia', 'avax_yieldyak', 'avax_gondola', 
                    'avax_swiftfinance', 'avax_smartcoin', 'avax_yetiswap', 'avax_penguin', 'avax_ribbon', 'avax_swamp', 'avax_pendle', 
                    'avax_dmm_exchange', 'avax_blizzard', 'avax_gmx', 'avax_singular', 'avax_autofarm', 'avax_elk', 'avax_iron2', 'avax_snowball', 
                    'avax_frost', 'avax_dune_frost', 'avax_partyswap', 'avax_cycle', 'avax_kuu', 'avax_cream', 'avax_olive', 'avax_avalaunch', 
                    'avax_canary', 'avax_curve', 'avax_avaware', 'avax_zero', 'avax_xdollar', 'avax_eleven', 'avax_dyp', 'avax_synapse', 'avax_stormswap', 
                    'avax_vee', 'avax_wonderland', 'avax_hurricaneswap', 'avax_hurricaneswap2', 'avax_thedragonslair', 'avax_teddy', 'avax_abracadabra', 
                    'avax_aave', 'avax_insurace', 'avax_traderjoexyz_lending', 'avax_instadapp', 'avax_alpha2', 'avax_wheat', 'avax_everestoptions', 
                    'avax_impermax', 'avax_mai', 'avax_orca', 'avax_kittyfinance', 'avax_snowbank', 'avax_blizz', 'avax_gro', 'avax_piggybankdao', 
                    'avax_stabilize', 'avax_relaychain', 'avax_snowdogdao', 'avax_fortressdao', 'avax_roco', 'avax_yieldwolf', 'avax_defrost', 
                    'avax_cook', 'avax_talecraft', 'avax_rugfarm', 'avax_maximizer', 'avax_galaxygoggle', 'avax_icedao', 'avax_marginswap', 'avax_papadao', 
                    'avax_colonylab', 'avax_lifedao', 'avax_midasdao', 'avax_olympusdao_pro', 'avax_platypus', 'avax_ragnarokdao', 'avax_stakedao', 
                    'avax_sushiswap', 'avax_vortexdao', 'avax_tempodao', 'avax_snowbear', 'avax_parrotdao', 'avax_pooltogether', 'avax_spiritdao', 
                    'avax_barnbridge', 'avax_louverture', 'avax_vapornodes', 'avax_magnetdao', 'avax_boofinance', 'avax_hermesfinance', 'avax_thornode', 
                    'avax_thorus', 'avax_kalao', 'op_curve', 'op_uniswap3', 'op_hop', 'op_synthetix', 'op_lyra', 'op_synapse', 'op_wepiggy', 
                    'op_dforcelending', 'arb_curve', 'arb_dforcelending', 'arb_wepiggy', 'arb_sushiswap', 'arb_uniswap3', 'arb_balancer2', 'arb_saddle', 
                    'arb_swapr', 'arb_dodoex', 'arb_carbon', 'arb_cream', 'arb_sushiswap_lending', 'arb_mcdex', 'arb_gmx', 'arb_dopex', 'arb_arbog', 
                    'arb_hop', 'arb_pickle', 'arb_arbinyan', 'arb_badger', 'arb_tracer', 'arb_magicland', 'arb_adamant', 'arb_barnbridge', 'arb_beefy', 
                    'arb_elk', 'arb_impermax', 'arb_abracadabra', 'arb_channels', 'arb_synapse', 'arb_hundred', 'arb_zerotwohm', 'arb_flux', 
                    'arb_dogsofelon', 'arb_umami', 'arb_treasure', 'celo_autofarm', 'celo_ubeswap', 'celo_beefy', 'celo_pooltogether', 'celo_symmetric', 
                    'celo_sushiswap', 'celo_celodex', 'celo_moola', 'celo_mobius', 'celo_yieldwolf', 'movr_autofarm', 'movr_elk', 'movr_sushiswap', 
                    'movr_solarbeam', 'movr_huckleberry', 'movr_kogefarm', 'movr_beefy', 'movr_relaychain', 'movr_zenlink', 'movr_romedao', 
                    'movr_thegrandbanks', 'movr_impermax', 'movr_fantohm', 'movr_wepiggy', 'movr_mai', 'movr_hundred', 'cro_autofarm', 'cro_vvs', 
                    'cro_elk', 'cro_crodex', 'cro_beefy', 'cro_cronaswap', 'cro_polycrystal', 'cro_stormswap', 'cro_dnadollar', 'cro_fortunedao', 
                    'cro_yieldwolf', 'cro_annex', 'cro_smolswap', 'cro_blackbird', 'cro_mmf', 'cro_adamant', 'cro_tectonic', 'cro_crowfi', 'cro_mimas', 
                    'cro_croblanc', 'boba_oolongswap', 'boba_synapse', 'boba_autofarm', 'boba_swapperchan', 'boba_senpaiswap', 'boba_bobagateway', 
                    'metis_netswap', 'metis_standard', 'metis_beefy', 'metis_tethys', 'metis_hadesmoney', 'metis_pickle', 'metis_oceanus', 
                    'metis_agoradefi', 'aurora_wannaswap', 'aurora_nearpad', 'aurora_vaporwave', 'aurora_rose', 'aurora_trisolaris', 'aurora_auroraswap', 
                    'aurora_pickle', 'aurora_smartpad', 'aurora_synapse', 'aurora_paprprintr', 'aurora_dodoex', 'aurora_empyrean', 'mobm_stellaswap', 
                    'mobm_zenlink', 'mobm_thorus', 'mobm_solarflare', 'mobm_beamswap', 'sbch_mistswap', 'sbch_benswap', 'sbch_tangoswap', 'sbch_tropical']
    
    
    
    def __init__(self
                 , wallet_id: Optional[str] = None, 
                 ):
        
        self.API_URL = "https://openapi.debank.com" 
        self.WALLET_ID = wallet_id
        
        # End Points Chain
        self.chain_information = self.API_URL + self.V1 + self.CHAIN + self.ID + '{}'
        self.supported_chain_list = self.API_URL + self.V1 + self.CHAIN + self.LIST
        
        # End Points Protocol
        self.protocol_information = self.API_URL + self.V1 + self.PROTOCOL + self.ID + '{}'
        self.list_of_protocol_information = self.API_URL + self.V1 + self.PROTOCOL + self.LIST
        
        # End Points Token
        self.token_information = self.API_URL + self.V1 + self.TOKEN + self.CHAIN_ID + '{}' + self.ADDRESS + '{}'     
        self.list_token_information = self.API_URL + self.V1 + self.TOKEN + self.LIST_BY_IDS + self.CHAIN_ID + '{}' + self.IDS + '{}'
        
        # End Points User
        self.user_chain_balance = self.API_URL + self.V1 + self.USER + self.CHAIN_BALANCE + self.ID + '{}' + self.CHAIN_ID + '{}'
        self.user_protocol = self.API_URL + self.V1 + self.USER + self.PROTOCOL + self.ID + '{}' + self.PROTOCOL_ID + '{}'
        self.user_complex_protocol_list = self.API_URL + self.V1 + self.USER + self.COMPLEX_PROTOCOL_LIST + self.ID + '{}' + self.AND_CHAIN + '{}'
        self.user_simple_protocol_list = self.API_URL + self.V1 + self.USER + self.SIMPLE_PROTOCOL_LIST + self.ID + '{}' + self.AND_CHAIN + '{}'
        self.user_token_balance = self.API_URL + self.V1 + self.USER + self.TOKEN + self.ID + '{}' + self.AND_CHAIN + '{}' + self.TOKEN_ID + '{}'
        self.user_token_list =  self.API_URL + self.V1 + self.USER + self.TOKEN_LIST +  self.ID + '{}' + self.AND_CHAIN + '{}' + self.IS_ALL + '{}' + self.HAS_BALANCE + '{}'
        self.search_user_token = self.API_URL + self.V1 + self.USER + self.TOKEN_SEARCH + self.CHAIN_ID + '{}' + self.ADDRESS + '{}' + self.Q + '{}' + self.HAS_BALANCE + '{}'
        self.user_total_balance = self.API_URL + self.V1 + self.USER + self.TOTAL_BALANCE + self.ID + '{}'
        



    def get_chain_information(self, chain):  
        """
        
        https://openapi.debank.com/docs
        
        Parameters
        ----------
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.

        Returns
        -------
        {
          "id": "eth",
          "community_id": 1,
          "name": "Ethereum",
          "logo_url": "https://static.debank.com/image/chain/logo_url/eth/6e0cd1f895af9836ee8c32cfc03bc279.png",
          "native_token_id": "eth",
          "wrapped_token_id": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
        }.

        """
        
        url = self.chain_information.format(chain)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))



    def get_supported_chain_list(self):  
        """
        
        https://openapi.debank.com/docs
        
        Returns
        -------
        {
            "id": "eth",
            "community_id": 1,
            "name": "Ethereum",
            "logo_url": "https://static.debank.com/image/chain/logo_url/eth/6e0cd1f895af9836ee8c32cfc03bc279.png",
            "native_token_id": "eth",
            "wrapped_token_id": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
          }

        """

        
        url = self.supported_chain_list
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))


    def get_protocol_information(self, protocol):  
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        protocol : bsc_pancakeswap, curve, uniswap, ecc.
            DESCRIPTION.

        Returns
        -------
        {
          "id": "compound",
          "chain_id": 1,
          "name": "Compound",
          "logo_url": "https://static.debank.com/image/project/logo_url/compound/b4b9c8de20952846a1c9dfcded47d0db.png",
          "site_url": "https://app.compound.finance",
          "has_supported_portfolio": true
        }

        """

        
        url = self.protocol_information.format(protocol)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))


    def get_list_of_protocol_information(self):  
        """
        https://openapi.debank.com/docs

        Parameters
        ----------


        Returns
        -------
         [
          {
            "id": "compound",
            "chain_id": 1,
            "name": "Compound",
            "logo_url": "https://static.debank.com/image/project/logo_url/compound/b4b9c8de20952846a1c9dfcded47d0db.png",
            "site_url": "https://app.compound.finance",
            "has_supported_portfolio": true
          }
        ]
        """

        
        url = self.list_of_protocol_information
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))


    def get_token_information(self, chain, address): 
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.
        address : string
            DESCRIPTION.

        Returns
        -------
        {
          "id": "0xdac17f958d2ee523a2206206994597c13d831ec7",
          "chain": 1,
          "name": "Tether USD",
          "symbol": "USDT",
          "decimals": 6,
          "logo_url": "https://static.debank.com/image/token/logo_url/0xdac17f958d2ee523a2206206994597c13d831ec7/3c1a718331e468abe1fc2ebe319f6c77.png",
          "is_verified": true,
          "price": 1.01,
          "is_wallet": true
        }

        """

        
        url = self.token_information.format(chain, address)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))
    

    def get_list_token_information(self, chain, address):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.
        address : list of addresses
            DESCRIPTION.

        Returns
        -------
        [
          {
            "id": "0xdac17f958d2ee523a2206206994597c13d831ec7",
            "chain": 1,
            "name": "Tether USD",
            "symbol": "USDT",
            "decimals": 6,
            "logo_url": "https://static.debank.com/image/token/logo_url/0xdac17f958d2ee523a2206206994597c13d831ec7/3c1a718331e468abe1fc2ebe319f6c77.png",
            "is_verified": true,
            "price": 1.01,
            "is_wallet": true
          }
        ]

        """

        
        url = self.list_token_information.format(chain, ','.join(address))
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))
        


    def get_chain_balance(self, address, chain):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
            
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.


        Returns
        -------
        return to the usd value of net assets

        """

        
        url = self.user_chain_balance.format(address, chain)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))
        
    def get_user_protocol(self, address, protocol):
        """
        

        Parameters
        ----------
        address : address
            DESCRIPTION.
        protocol : bsc_pancakeswap, curve, uniswap, ecc.
            DESCRIPTION.

        Returns
        -------
        {
          "id": "compound",
          "chain": "eth",
          "name": "Compound",
          "site_url": "https://app.compound.finance",
          "logo_url": "https://static.debank.com/image/project/logo_url/compound/0b792243f1f68e9ed082f5a49ee6f21d.png",
          "has_supported_portfolio": true,
          "tvl": 12763095483.420198
        }

        """
        
        url = self.user_protocol.format(address, protocol)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))        


    def get_user_complex_protocol_list(self, address, chain):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.

        Returns
        -------
        return the list of protocol with user’s portfolio items

        """
        
        url = self.user_complex_protocol_list.format(address, chain)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))        


    def get_user_simple_protocol_list(self, address, chain):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.

        Returns
        -------
        	
        return list of protocols with user assets

        """
        
        url = self.user_simple_protocol_list.format(address, chain)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))        


    def get_user_token_balance(self, address, chain, token_address):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.
        token_address : token_address
            DESCRIPTION.            

        Returns
        -------
        	
        return list of protocols with user assets

        """
        
        url = self.user_token_balance.format(address, chain, token_address)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))   



    def get_user_token_list(self, address, chain, is_all = 'true', has_balance = 'true'):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.
        is_all: Boolean, true or false. If true, all tokens are returned, including protocol-derived tokens
        Returns
        -------
        	
        return list of protocols with user assets

        """
        
        url = self.user_token_list.format(address, chain, is_all, has_balance)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))  
    
    

    def get_search_user_token(self, chain, address, q, has_balance = 'true'):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
        chain : eth, bsc, xdai, matic, ftm, okt, heco, avax, op, arb, celo, movr, cro, boba, metis, btt, aurora, mobm, sbch
            DESCRIPTION.
        q: string. filter args
        has_balance: Boolean, true or false. If true, only token with balance will returned.
        
        Returns
        -------
        	
        return list of protocols with user assets

        """
        
        url = self.search_user_token.format(chain, address, q, has_balance)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))       
    
    

    def get_total_balance(self, address):
        """
        https://openapi.debank.com/docs

        Parameters
        ----------
        address : address
            DESCRIPTION.
        
        Returns
        -------
        	
        return the total net assets and the net assets of each chain

        """
        
        url = self.user_total_balance.format(address)
        res = requests.get(url, headers = {'Content-Type' : self.OPTION_REQ})
        return eval(res.text.replace('null', "'null'").replace('true',"'true'"))    

        




wallet = Wallet()
test = wallet.get_user_token_list("0x1223D1B5D7Bc6049e1A4E7e60079803496E73029", 'ftm')









