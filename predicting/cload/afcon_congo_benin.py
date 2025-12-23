# afcon_predictor_optimized.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

class OptimizedAFCONPredictor:
    """Optimized AFCON 2025 predictor with enhanced accuracy"""
    
    def __init__(self):
        plt.style.use('default')
        
        # Calibrated tournament constants
        self.AVG_GOALS_AFCON = 1.28
        self.CORRELATION_RHO = -0.15
        
        # Complete team database
        self.TEAMS = {
            'Congo DR': {
                'fifa_rank': 62, 'elo': 1620, 'team_strength_index': 0.64,
                'attack_strength': 1.32, 'defense_strength': 1.10,
                'avg_goals': 1.45, 'avg_conceded': 1.05,
                'xg_for': 1.55, 'xg_against': 1.10,
                'shots_per_match': 11.8, 'shots_on_target': 4.7,
                'possession': 48.5, 'pass_accuracy': 82.3,
                'form_last_5': [1, 0.5, 1, 1, 0.5],
                'goals_last_5': 7, 'conceded_last_5': 4, 'clean_sheets_last_5': 2,
                'squad_value_million_eur': 170, 'avg_player_rating': 6.9,
                'players_top5_leagues': 7, 'avg_age': 26.8,
                'injury_index': 0.15, 'star_dependency': 0.34,
                'pressing_intensity': 0.58, 'defensive_line_height': 0.46,
                'counter_attack_rate': 0.62, 'set_piece_goals_ratio': 0.28,
                'coach_experience_years': 12, 'squad_afcon_experience': 0.62,
                'knockout_win_rate': 0.48, 'variance_index': 0.32,
                'coach': 'Sébastien Desabre', 'key_player': 'Yoane Wissa',
                'style': 'Physical, direct', 'weakness': 'Inconsistent finishing',
                'colors': {'primary': '#0088CE', 'secondary': '#FFD700'}
            },
            'Benin': {
                'fifa_rank': 88, 'elo': 1520, 'team_strength_index': 0.52,
                'attack_strength': 1.05, 'defense_strength': 1.12,
                'avg_goals': 1.10, 'avg_conceded': 1.30,
                'xg_for': 1.18, 'xg_against': 1.32,
                'shots_per_match': 9.4, 'shots_on_target': 3.5,
                'possession': 44.2, 'pass_accuracy': 78.6,
                'form_last_5': [0.5, 0, 1, 0.5, 0],
                'goals_last_5': 5, 'conceded_last_5': 7, 'clean_sheets_last_5': 1,
                'squad_value_million_eur': 50, 'avg_player_rating': 6.6,
                'players_top5_leagues': 3, 'avg_age': 27.4,
                'injury_index': 0.18, 'star_dependency': 0.42,
                'pressing_intensity': 0.46, 'defensive_line_height': 0.38,
                'counter_attack_rate': 0.68, 'set_piece_goals_ratio': 0.31,
                'coach_experience_years': 20, 'squad_afcon_experience': 0.55,
                'knockout_win_rate': 0.36, 'variance_index': 0.38,
                'coach': 'Gernot Rohr', 'key_player': 'Steve Mounié',
                'style': 'Defensive, counter-attack', 'weakness': 'Goal scoring',
                'colors': {'primary': '#008751', 'secondary': '#FF0000'}
            },
            'Senegal': {
                'fifa_rank': 20, 'elo': 1750, 'team_strength_index': 0.78,
                'attack_strength': 1.48, 'defense_strength': 0.95,
                'avg_goals': 1.60, 'avg_conceded': 0.85,
                'xg_for': 1.65, 'xg_against': 0.90,
                'shots_per_match': 13.2, 'shots_on_target': 5.2,
                'possession': 52.8, 'pass_accuracy': 84.6,
                'form_last_5': [1, 1, 0.5, 1, 1],
                'goals_last_5': 8, 'conceded_last_5': 3, 'clean_sheets_last_5': 3,
                'squad_value_million_eur': 350, 'avg_player_rating': 7.2,
                'players_top5_leagues': 15, 'avg_age': 27.1,
                'injury_index': 0.12, 'star_dependency': 0.38,
                'pressing_intensity': 0.62, 'defensive_line_height': 0.50,
                'counter_attack_rate': 0.55, 'set_piece_goals_ratio': 0.30,
                'coach_experience_years': 9, 'squad_afcon_experience': 0.78,
                'knockout_win_rate': 0.65, 'variance_index': 0.28,
                'coach': 'Aliou Cissé', 'key_player': 'Sadio Mané',
                'style': 'Balanced, high intensity', 'weakness': 'Occasional creativity drop',
                'colors': {'primary': '#00853F', 'secondary': '#FDEF42'}
            },
            'Botswana': {
                'fifa_rank': 147, 'elo': 1380, 'team_strength_index': 0.36,
                'attack_strength': 0.85, 'defense_strength': 1.25,
                'avg_goals': 0.85, 'avg_conceded': 1.65,
                'xg_for': 0.90, 'xg_against': 1.70,
                'shots_per_match': 7.8, 'shots_on_target': 2.6,
                'possession': 41.0, 'pass_accuracy': 75.2,
                'form_last_5': [0, 0.5, 0, 1, 0],
                'goals_last_5': 3, 'conceded_last_5': 8, 'clean_sheets_last_5': 1,
                'squad_value_million_eur': 18, 'avg_player_rating': 6.2,
                'players_top5_leagues': 0, 'avg_age': 26.5,
                'injury_index': 0.20, 'star_dependency': 0.46,
                'pressing_intensity': 0.40, 'defensive_line_height': 0.34,
                'counter_attack_rate': 0.70, 'set_piece_goals_ratio': 0.34,
                'coach_experience_years': 7, 'squad_afcon_experience': 0.22,
                'knockout_win_rate': 0.18, 'variance_index': 0.45,
                'coach': 'Didier Gomes Da Rosa', 'key_player': 'Thapelo Kopelang',
                'style': 'Low block, counter-attack', 'weakness': 'Defensive transitions',
                'colors': {'primary': '#75AADB', 'secondary': '#000000'}
            }
        }
    
    def calculate_elo_expectation(self, elo_home, elo_away):
        """Calculate match outcome probability from Elo ratings"""
        elo_diff = elo_home - elo_away
        expected_home = 1 / (1 + 10 ** (-elo_diff / 400))
        return expected_home
    
    def calculate_optimized_lambda(self, home_data, away_data):
        """Calculate expected goals with optimized weighting"""
        
        # Base attack vs defense
        lambda_home_base = home_data['xg_for'] * (2.0 - away_data['defense_strength'])
        lambda_away_base = away_data['xg_for'] * (2.0 - home_data['defense_strength'])
        
        # Form factor (exponential recency weighting)
        weights = np.array([0.40, 0.30, 0.20, 0.07, 0.03])
        home_form = np.dot(home_data['form_last_5'], weights)
        away_form = np.dot(away_data['form_last_5'], weights)
        form_factor = 1 + (home_form - away_form) * 0.35
        
        # Quality adjustment using multiple metrics
        elo_advantage = self.calculate_elo_expectation(home_data['elo'], away_data['elo'])
        squad_ratio = np.log1p(home_data['squad_value_million_eur']) / np.log1p(away_data['squad_value_million_eur'])
        quality_factor = (elo_advantage - 0.5) * 2  # Normalize to -1 to 1
        
        # xG over/underperformance
        home_xg_ratio = home_data['avg_goals'] / max(home_data['xg_for'], 0.5)
        away_xg_ratio = away_data['avg_goals'] / max(away_data['xg_for'], 0.5)
        
        # Tactical matchup
        pressing_advantage = home_data['pressing_intensity'] - away_data['pressing_intensity']
        tactical_home = 1 + pressing_advantage * 0.15
        tactical_away = 1 - pressing_advantage * 0.12
        
        # Style matchup
        if away_data['counter_attack_rate'] > 0.65 and home_data['defensive_line_height'] > 0.45:
            style_home = 0.92
            style_away = 1.12
        elif home_data['counter_attack_rate'] > 0.65 and away_data['defensive_line_height'] > 0.45:
            style_home = 1.12
            style_away = 0.92
        else:
            style_home = 1.0
            style_away = 1.0
        
        # Calculate final lambdas
        lambda_home = (
            lambda_home_base *
            (1 + quality_factor * 0.30) *
            form_factor *
            (0.7 + home_xg_ratio * 0.3) *
            tactical_home *
            style_home *
            (1 - home_data['variance_index'] * 0.15) *
            (1 - home_data['injury_index'] * 0.20)
        )
        
        lambda_away = (
            lambda_away_base *
            (1 - quality_factor * 0.25) *
            (2 - form_factor) *
            (0.7 + away_xg_ratio * 0.3) *
            tactical_away *
            style_away *
            (1 - away_data['variance_index'] * 0.15) *
            (1 - away_data['injury_index'] * 0.20)
        )
        
        # AFCON-specific calibration
        lambda_home *= 0.92
        lambda_away *= 0.88
        
        # Ensure realistic bounds
        lambda_home = np.clip(lambda_home, 0.25, 3.2)
        lambda_away = np.clip(lambda_away, 0.20, 2.8)
        
        return lambda_home, lambda_away
    
    def bivariate_poisson_enhanced(self, lambda_home, lambda_away, max_goals=6):
        """Enhanced bivariate Poisson with AFCON-specific adjustments"""
        
        rho = self.CORRELATION_RHO
        probs = np.zeros((max_goals + 1, max_goals + 1))
        
        for i in range(max_goals + 1):
            for j in range(max_goals + 1):
                # Base independent Poisson
                p_indep = stats.poisson.pmf(i, lambda_home) * stats.poisson.pmf(j, lambda_away)
                
                # Bivariate correlation adjustment
                if i == 0 and j == 0:
                    corr_factor = np.exp(rho * lambda_home * lambda_away)
                elif i == 0 or j == 0:
                    corr_factor = 1 + rho * lambda_home * lambda_away / 2
                elif i == 1 and j == 1:
                    corr_factor = 1 - rho
                else:
                    corr_factor = 1.0
                
                # AFCON-specific adjustments
                afcon_boost = 1.0
                if i == 0 and j == 0:
                    afcon_boost = 1.32
                elif i == 1 and j == 0:
                    afcon_boost = 1.25
                elif i == 0 and j == 1:
                    afcon_boost = 1.20
                elif i == 1 and j == 1:
                    afcon_boost = 1.18
                elif i == 2 and j == 0:
                    afcon_boost = 1.10
                elif i == 0 and j == 2:
                    afcon_boost = 1.05
                elif i == 2 and j == 1:
                    afcon_boost = 1.08
                elif i + j > 4:
                    afcon_boost = 0.75
                
                probs[i, j] = p_indep * corr_factor * afcon_boost
        
        # Normalize
        probs = probs / probs.sum()
        
        return probs
    
    def ensemble_prediction(self, home_data, away_data):
        """Ensemble multiple methods for robust prediction"""
        
        # Method 1: Optimized Poisson
        lambda_h1, lambda_a1 = self.calculate_optimized_lambda(home_data, away_data)
        probs1 = self.bivariate_poisson_enhanced(lambda_h1, lambda_a1)
        
        # Method 2: Conservative estimate
        lambda_h2 = lambda_h1 * 0.90
        lambda_a2 = lambda_a1 * 0.90
        probs2 = self.bivariate_poisson_enhanced(lambda_h2, lambda_a2)
        
        # Method 3: Aggressive estimate
        quality_boost = (home_data['team_strength_index'] / away_data['team_strength_index'])
        lambda_h3 = lambda_h1 * min(quality_boost, 1.15)
        lambda_a3 = lambda_a1 * min(1/quality_boost, 1.10)
        probs3 = self.bivariate_poisson_enhanced(lambda_h3, lambda_a3)
        
        # Weighted ensemble
        probs_ensemble = (probs1 * 0.55 + probs2 * 0.25 + probs3 * 0.20)
        probs_ensemble = probs_ensemble / probs_ensemble.sum()
        
        # Final calibration
        probs_ensemble[0, 0] *= 1.05
        probs_ensemble[1, 0] *= 1.08
        probs_ensemble[0, 1] *= 1.06
        probs_ensemble[1, 1] *= 1.04
        probs_ensemble = probs_ensemble / probs_ensemble.sum()
        
        return probs_ensemble, (lambda_h1, lambda_a1)
    
    def predict_match(self, home_team, away_team):
        """Main prediction function"""
        
        if home_team not in self.TEAMS or away_team not in self.TEAMS:
            print(f"Error: Team not found. Available teams: {', '.join(self.TEAMS.keys())}")
            return None
        
        home_data = self.TEAMS[home_team]
        away_data = self.TEAMS[away_team]
        
        print(f"\n{'='*100}")
        print(f"🏆 OPTIMIZED AFCON 2025 PREDICTION: {home_team} vs {away_team}")
        print(f"{'='*100}\n")
        
        # Team comparison
        print(f"📊 TEAM COMPARISON")
        print(f"{'-'*100}")
        print(f"{'Metric':<25} {home_team:<30} {away_team:<30} {'Advantage':<15}")
        print(f"{'-'*100}")
        
        comparisons = [
            ('FIFA Rank', f"#{home_data['fifa_rank']}", f"#{away_data['fifa_rank']}"),
            ('Elo Rating', f"{home_data['elo']}", f"{away_data['elo']}"),
            ('Squad Value', f"€{home_data['squad_value_million_eur']}M", f"€{away_data['squad_value_million_eur']}M"),
            ('Attack Strength', f"{home_data['attack_strength']:.2f}", f"{away_data['attack_strength']:.2f}"),
            ('Defense Strength', f"{home_data['defense_strength']:.2f}", f"{away_data['defense_strength']:.2f}"),
            ('Avg Goals', f"{home_data['avg_goals']:.2f}", f"{away_data['avg_goals']:.2f}"),
            ('Form (Last 5)', f"{np.mean(home_data['form_last_5']):.2f}", f"{np.mean(away_data['form_last_5']):.2f}"),
            ('Top 5 Leagues', f"{home_data['players_top5_leagues']}", f"{away_data['players_top5_leagues']}"),
            ('AFCON Experience', f"{home_data['squad_afcon_experience']:.2f}", f"{away_data['squad_afcon_experience']:.2f}"),
        ]
        
        for metric, home_val, away_val in comparisons:
            try:
                if '#' in home_val:
                    h_num = int(home_val[1:])
                    a_num = int(away_val[1:])
                    adv = home_team if h_num < a_num else (away_team if h_num > a_num else "Equal")
                elif '€' in home_val or 'M' in home_val:
                    h_num = float(home_val.replace('€','').replace('M',''))
                    a_num = float(away_val.replace('€','').replace('M',''))
                    adv = home_team if h_num > a_num else (away_team if h_num < a_num else "Equal")
                else:
                    h_num = float(home_val)
                    a_num = float(away_val)
                    adv = home_team if h_num > a_num else (away_team if h_num < a_num else "Equal")
            except:
                adv = "-"
            
            print(f"{metric:<25} {home_val:<30} {away_val:<30} {adv:<15}")
        
        print(f"\n{'='*100}\n")
        
        # Get prediction
        probs, (lambda_home, lambda_away) = self.ensemble_prediction(home_data, away_data)
        
        # Find most likely score
        max_idx = np.unravel_index(np.argmax(probs), probs.shape)
        predicted_score = f"{max_idx[0]}-{max_idx[1]}"
        confidence = probs[max_idx] * 100
        
        # Calculate outcomes
        home_win = np.sum(np.triu(probs, k=1)) * 100
        draw = np.sum(np.diag(probs)) * 100
        away_win = np.sum(np.tril(probs, k=-1)) * 100
        
        # Get top scores
        flat_indices = np.argsort(probs.flatten())[::-1][:15]
        top_scores = []
        cumulative = 0
        for idx in flat_indices:
            h, a = np.unravel_index(idx, probs.shape)
            prob = probs[h, a] * 100
            cumulative += prob
            top_scores.append({
                'score': f"{h}-{a}",
                'probability': prob,
                'cumulative': cumulative
            })
        
        # Display results
        print("🎯 OPTIMIZED PREDICTION RESULTS")
        print(f"{'='*100}\n")
        print(f"🏆 Most Likely Score: {predicted_score}")
        print(f"📊 Model Confidence: {confidence:.2f}%\n")
        print(f"⚽ Expected Goals:")
        print(f"   {home_team}: {lambda_home:.2f}")
        print(f"   {away_team}: {lambda_away:.2f}\n")
        print(f"📈 Match Outcome Probabilities:")
        print(f"   {home_team} Win: {home_win:.2f}%")
        print(f"   Draw: {draw:.2f}%")
        print(f"   {away_team} Win: {away_win:.2f}%\n")
        
        print(f"🔝 Top 15 Most Probable Scores:")
        print(f"{'-'*80}")
        print(f"{'Rank':<8} {'Score':<12} {'Probability':<18} {'Cumulative':<18} {'1 in X':<12}")
        print(f"{'-'*80}")
        
        for i, s in enumerate(top_scores, 1):
            expected = int(100/s['probability']) if s['probability'] > 0 else 999
            print(f"{i:<8} {s['score']:<12} {s['probability']:>6.2f}%{'':<10} {s['cumulative']:>6.2f}%{'':<10} {expected:<12}")
        
        print(f"\n{'='*100}")
        print("💡 KEY INSIGHTS:")
        
        # Strength difference
        strength_diff = home_data['team_strength_index'] - away_data['team_strength_index']
        squad_ratio = home_data['squad_value_million_eur'] / away_data['squad_value_million_eur']
        
        print(f"   • Strength Index: {home_team} {home_data['team_strength_index']:.2f} vs {away_team} {away_data['team_strength_index']:.2f} ({strength_diff:+.2f})")
        print(f"   • Squad Value Ratio: {squad_ratio:.1f}x in favor of {home_team if squad_ratio > 1 else away_team}")
        print(f"   • Form: {home_team} {np.mean(home_data['form_last_5']):.2f} vs {away_team} {np.mean(away_data['form_last_5']):.2f}")
        print(f"   • Style: {home_data['style']} vs {away_data['style']}")
        print(f"   • Key Players: {home_data['key_player']} vs {away_data['key_player']}")
        print(f"   • AFCON Average: {self.AVG_GOALS_AFCON} goals/team (typically low-scoring)")
        
        # Tactical insight
        if abs(strength_diff) > 0.3:
            print(f"   • Clear favorite: {home_team if strength_diff > 0 else away_team}")
        else:
            print(f"   • Evenly matched - tactical battle expected")
        
        print(f"{'='*100}\n")
        
        return {
            'match': f"{home_team} vs {away_team}",
            'predicted_score': predicted_score,
            'confidence': round(confidence, 2),
            'expected_goals': {'home': round(lambda_home, 2), 'away': round(lambda_away, 2)},
            'outcomes': {'home_win': round(home_win, 2), 'draw': round(draw, 2), 'away_win': round(away_win, 2)},
            'top_scores': top_scores,
            'team_data': {
                'home': {
                    'team': home_team,
                    'coach': home_data['coach'],
                    'key_player': home_data['key_player'],
                    'style': home_data['style']
                },
                'away': {
                    'team': away_team,
                    'coach': away_data['coach'],
                    'key_player': away_data['key_player'],
                    'style': away_data['style']
                }
            }
        }

# Main execution
if __name__ == "__main__":
    predictor = OptimizedAFCONPredictor()
    
    print("\n🏆 AFCON 2025 OPTIMIZED PREDICTION SYSTEM")
    print("Available teams: Congo DR, Benin, Senegal, Botswana\n")
    
    # Example predictions
    print("="*100)
    print("MATCH 1: Congo DR vs Benin")
    print("="*100)
    result1 = predictor.predict_match('Congo DR', 'Benin')
    
    print("\n\n")
    print("="*100)
    print("MATCH 2: Senegal vs Botswana")
    print("="*100)
    result2 = predictor.predict_match('Senegal', 'Botswana')
    
    # Save results
    results = {
        'match_1': result1,
        'match_2': result2,
        'model_info': {
            'name': 'Optimized AFCON 2025 Predictor',
            'version': '2.0',
            'timestamp': datetime.now().isoformat()
        }
    }
    
    with open('afcon_predictions.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n\n💾 Predictions saved to: afcon_predictions.json")