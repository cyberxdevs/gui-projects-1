"""
Export Utilities - Export hasil analisis ke CSV
"""
import pandas as pd
import os
from datetime import datetime


def export_to_csv(analysis_results, user_name, output_dir='exports'):
    """
    Export hasil analisis ke CSV

    Args:
        analysis_results (dict): Dictionary hasil analisis
        user_name (str): Nama user
        output_dir (str): Directory output

    Returns:
        str: Path ke file CSV yang dibuat
    """
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Prepare data for table
    table_data = []

    # Get imbalance data
    imbalance = analysis_results.get('imbalance', {})

    # Shoulder
    if 'shoulder' in imbalance:
        table_data.append({
            'Komponen': 'Shoulder Imbalance',
            'Parameter': 'Perbedaan Tinggi Bahu',
            'Nilai': f"{imbalance['shoulder']:.1f}",
            'Satuan': 'mm',
            'Status': get_status('shoulder', imbalance['shoulder']),
            'Score': get_component_score('shoulder', imbalance['shoulder'])
        })

    # Hip
    if 'hip' in imbalance:
        table_data.append({
            'Komponen': 'Hip Imbalance',
            'Parameter': 'Perbedaan Tinggi Pinggul',
            'Nilai': f"{imbalance['hip']:.1f}",
            'Satuan': 'mm',
            'Status': get_status('hip', imbalance['hip']),
            'Score': get_component_score('hip', imbalance['hip'])
        })

    # Spine
    if 'spine' in imbalance:
        table_data.append({
            'Komponen': 'Spine Imbalance',
            'Parameter': 'Deviasi Tulang Belakang',
            'Nilai': f"{imbalance['spine']:.1f}",
            'Satuan': 'mm',
            'Status': get_status('spine', imbalance['spine']),
            'Score': get_component_score('spine', imbalance['spine'])
        })

    # Head shift
    if 'head_shift' in imbalance:
        table_data.append({
            'Komponen': 'Head Shift',
            'Parameter': 'Pergeseran Kepala',
            'Nilai': f"{imbalance['head_shift']:.1f}",
            'Satuan': 'mm',
            'Status': get_status('head_shift', imbalance['head_shift']),
            'Score': get_component_score('head_shift', imbalance['head_shift'])
        })

    # Head tilt
    if 'head_tilt' in imbalance:
        table_data.append({
            'Komponen': 'Head Tilt',
            'Parameter': 'Kemiringan Kepala',
            'Nilai': f"{imbalance['head_tilt']:.1f}",
            'Satuan': '°',
            'Status': get_status('head_tilt', imbalance['head_tilt']),
            'Score': get_component_score('head_tilt', imbalance['head_tilt'])
        })

    # Overall score
    overall_score = analysis_results.get('score', 0)
    table_data.append({
        'Komponen': 'OVERALL',
        'Parameter': 'Total Score',
        'Nilai': f"{overall_score:.1f}",
        'Satuan': '/100',
        'Status': get_overall_status(overall_score),
        'Score': f"{overall_score:.1f}"
    })

    # Create DataFrame
    df = pd.DataFrame(table_data)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{user_name}_{timestamp}_analisis_postur.csv"
    filepath = os.path.join(output_dir, filename)

    # Save to CSV
    df.to_csv(filepath, index=False, encoding='utf-8-sig')

    return filepath


def get_status(component, value):
    """
    Get status label berdasarkan komponen dan nilai

    Args:
        component (str): Nama komponen
        value (float): Nilai pengukuran

    Returns:
        str: Status label
    """
    if component in ['shoulder', 'hip', 'spine', 'head_shift']:
        if value < 10:
            return 'Normal'
        elif value < 20:
            return 'Ringan'
        elif value < 30:
            return 'Sedang'
        else:
            return 'Berat'
    elif component == 'head_tilt':
        if value < 5:
            return 'Normal'
        elif value < 10:
            return 'Ringan'
        elif value < 15:
            return 'Sedang'
        else:
            return 'Berat'

    return 'Unknown'


def get_component_score(component, value):
    """
    Calculate score untuk komponen

    Args:
        component (str): Nama komponen
        value (float): Nilai pengukuran

    Returns:
        str: Score string
    """
    if component in ['shoulder', 'hip', 'spine', 'head_shift']:
        if value < 10:
            score = 100
        elif value < 20:
            score = 75
        elif value < 30:
            score = 50
        else:
            score = 25
    elif component == 'head_tilt':
        if value < 5:
            score = 100
        elif value < 10:
            score = 75
        elif value < 15:
            score = 50
        else:
            score = 25
    else:
        score = 0

    return f"{score}/100"


def get_overall_status(score):
    """
    Get overall status berdasarkan score

    Args:
        score (float): Overall score

    Returns:
        str: Status label
    """
    if score >= 80:
        return 'Excellent'
    elif score >= 60:
        return 'Good'
    elif score >= 40:
        return 'Fair'
    elif score >= 20:
        return 'Poor'
    else:
        return 'Critical'
