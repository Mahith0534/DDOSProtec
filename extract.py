import pandas as pd

def parse_zeek_log(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    header_lines = [line for line in lines if line.startswith('#')]
    data_lines = [line for line in lines if not line.startswith('#') and line.strip()]

    fields_line = next(line for line in header_lines if line.startswith('#fields'))
    fields = fields_line.strip().split('\t')[1:]

    data = [dict(zip(fields, line.strip().split('\t'))) for line in data_lines]

    return pd.DataFrame(data)

# Load conn.log and flowmeter.log
conn_df = parse_zeek_log("conn.log")
flow_df = parse_zeek_log("flowmeter.log")

# Select and rename fields from conn.log
conn_selected = conn_df[['uid', 'id.orig_h','id.orig_p', 'id.resp_p', 'proto']].copy()
conn_selected = conn_selected.rename(columns={
    'id.orig_h': 'Src IP',
    'id.orig_p': 'Src Port',
    'id.resp_p': 'Dst Port',
    'proto': 'Protocol'
})
conn_selected.loc[:, 'Src IP'] = conn_selected['Src IP'].astype(str)
conn_selected.loc[:, 'Src Port'] = conn_selected['Src Port'].astype(int)
conn_selected.loc[:, 'Dst Port'] = conn_selected['Dst Port'].astype(int)
conn_selected.loc[:, 'Protocol'] = conn_selected['Protocol'].map({'tcp': 6, 'udp': 17, 'icmp': 1}).fillna(0).astype(int)

# Select and rename fields from flowmeter.log
flow_selected = flow_df[[
    'uid',
    'flow_duration',
    'fwd_pkts_tot', 'bwd_pkts_tot',
    'fwd_pkts_per_sec', 'bwd_pkts_per_sec', 'flow_pkts_per_sec',
    'down_up_ratio',
    'flow_FIN_flag_count', 'flow_SYN_flag_count', 'flow_RST_flag_count',
    'fwd_PSH_flag_count', 'flow_ACK_flag_count',
    'fwd_URG_flag_count',
    'flow_CWR_flag_count', 'flow_ECE_flag_count',
    'fwd_subflow_pkts', 'bwd_subflow_pkts',
    'fwd_subflow_bytes', 'bwd_subflow_bytes',
    'active.avg', 'active.std', 'active.max', 'active.min',
    'idle.avg', 'idle.std', 'idle.max', 'idle.min',
    'fwd_pkts_payload.max', 'fwd_pkts_payload.min', 'fwd_pkts_payload.avg', 'fwd_pkts_payload.std',
    'bwd_pkts_payload.max', 'bwd_pkts_payload.min', 'bwd_pkts_payload.avg', 'bwd_pkts_payload.std',
    'payload_bytes_per_second'
]].copy()

flow_selected = flow_selected.rename(columns={
    'flow_duration': 'Flow Duration',
    'fwd_pkts_tot': 'Tot Fwd Pkts',
    'bwd_pkts_tot': 'Tot Bwd Pkts',
    'fwd_pkts_payload.max': 'Fwd Pkt Len Max',
    'fwd_pkts_payload.min': 'Fwd Pkt Len Min',
    'fwd_pkts_payload.avg': 'Fwd Pkt Len Mean',
    'fwd_pkts_payload.std': 'Fwd Pkt Len Std',
    'bwd_pkts_payload.max': 'Bwd Pkt Len Max',
    'bwd_pkts_payload.min': 'Bwd Pkt Len Min',
    'bwd_pkts_payload.avg': 'Bwd Pkt Len Mean',
    'bwd_pkts_payload.std': 'Bwd Pkt Len Std',
    'payload_bytes_per_second': 'Flow Byts/s',
    'flow_pkts_per_sec': 'Flow Pkts/s',
    'fwd_pkts_per_sec': 'Fwd Pkts/s',
    'bwd_pkts_per_sec': 'Bwd Pkts/s',
    'down_up_ratio': 'Down/Up Ratio',
    'flow_FIN_flag_count': 'FIN Flag Cnt',
    'flow_SYN_flag_count': 'SYN Flag Cnt',
    'flow_RST_flag_count': 'RST Flag Cnt',
    'fwd_PSH_flag_count': 'PSH Flag Cnt',
    'flow_ACK_flag_count': 'ACK Flag Cnt',
    'fwd_URG_flag_count': 'URG Flag Cnt',
    'flow_CWR_flag_count': 'CWE Flag Count',
    'flow_ECE_flag_count': 'ECE Flag Cnt',
    'fwd_subflow_pkts': 'Subflow Fwd Pkts',
    'bwd_subflow_pkts': 'Subflow Bwd Pkts',
    'fwd_subflow_bytes': 'Subflow Fwd Byts',
    'bwd_subflow_bytes': 'Subflow Bwd Byts',
    'active.avg': 'Active Mean',
    'active.std': 'Active Std',
    'active.max': 'Active Max',
    'active.min': 'Active Min',
    'idle.avg': 'Idle Mean',
    'idle.std': 'Idle Std',
    'idle.max': 'Idle Max',
    'idle.min': 'Idle Min'
})

# Convert all columns except 'uid' to numeric
for col in flow_selected.columns:
    if col != 'uid':
        flow_selected.loc[:, col] = pd.to_numeric(flow_selected[col], errors='coerce')

# Merge datasets
merged_df = pd.merge(conn_selected, flow_selected, on='uid')

# Drop rows with any NaNs (to remove rows with missing data)
merged_df = merged_df.dropna()

# Desired column order (exactly 39 columns)
desired_order = [
    'Src IP', 'Src Port', 'Dst Port', 'Protocol', 'Flow Duration', 'Tot Fwd Pkts',
    'Tot Bwd Pkts', 'Fwd Pkt Len Max', 'Fwd Pkt Len Min',
    'Fwd Pkt Len Mean', 'Fwd Pkt Len Std', 'Bwd Pkt Len Max',
    'Bwd Pkt Len Min', 'Bwd Pkt Len Mean', 'Bwd Pkt Len Std', 'Flow Byts/s',
    'Flow Pkts/s', 'Fwd Pkts/s', 'Bwd Pkts/s', 'Down/Up Ratio',
    'FIN Flag Cnt', 'SYN Flag Cnt', 'RST Flag Cnt', 'PSH Flag Cnt',
    'ACK Flag Cnt', 'URG Flag Cnt', 'CWE Flag Count', 'ECE Flag Cnt',
    'Subflow Fwd Pkts', 'Subflow Bwd Pkts', 'Subflow Fwd Byts',
    'Subflow Bwd Byts', 'Active Mean', 'Active Std', 'Active Max',
    'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min'
]

# Ensure only the required columns are present in order
merged_df = merged_df[desired_order]

# Save to CSV
merged_df.to_csv("zeek_features.csv", index=False)

