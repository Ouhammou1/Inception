# afcon_nigeria_tanzania.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

class AFCON2025Predictor:
    """Advanced AFCON 2025 predictor with detailed team metrics"""
    
    def __init__(self):
        plt.style.use('default')
        
        # Tournament constants
        self.AVG_GOALS_AFCON = 1.35
        self.DRAWS_AFCON = 0.32
        self.LOW_SCORING_BOOST = 1.15
        
        # Morocco 2025 venues
        self.VENUES = {
            'Rabat': {'stadium': 'Prince Moulay Abdellah Stadium', 'capacity': 53000, 'temp': 17, 'humidity': 72, 'altitude': 135},
            'Casablanca': {'stadium': 'Stade Mohammed V', 'capacity': 45000, 'temp': 16, 'humidity': 75, 'altitude': 27},
            'Marrakech': {'stadium': 'Stade de Marrakech', 'capacity': 45240, 'temp': 19, 'humidity': 60, 'altitude': 466},
            'Tangier': {'stadium': 'Ibn Batouta Stadium', 'capacity': 45000, 'temp': 15, 'humidity': 78, 'altitude': 80},
            'Agadir': {'stadium': 'Stade Adrar', 'capacity': 45380, 'temp': 18, 'humidity': 70, 'altitude': 74}
        }
        
        # Detailed team data for Nigeria and Tanzania
        self.TEAMS = {
            'Nigeria': {
                # Rankings & global strength
                'fifa_rank': 42,
                'elo': 1680,
                'team_strength_index': 0.72,

                # Attack & defense
                'attack_strength': 1.45,
                'defense_strength': 1.08,
                'attack_defense_ratio': 1.34,

                # Goals & expected goals
                'avg_goals': 1.60,
                'avg_conceded': 1.10,
                'xg_for': 1.65,
                'xg_against': 1.15,

                # Shooting & possession
                'shots_per_match': 12.5,
                'shots_on_target': 5.2,
                'possession': 52.3,
                'pass_accuracy': 83.7,

                # Recent form (last 5 matches) - W=1 D=0.5 L=0
                'form_last_5': [1, 0.5, 1, 0, 1],
                'goals_last_5': 9,
                'conceded_last_5': 5,
                'clean_sheets_last_5': 2,

                # Squad quality
                'squad_value_million_eur': 380,
                'avg_player_rating': 7.1,
                'players_top5_leagues': 12,
                'avg_age': 26.2,
                'injury_index': 0.12,
                'star_dependency': 0.38,

                # Tactical metrics
                'pressing_intensity': 0.62,
                'defensive_line_height': 0.52,
                'counter_attack_rate': 0.58,
                'set_piece_goals_ratio': 0.32,

                # Experience & psychology
                'coach_experience_years': 8,
                'squad_afcon_experience': 0.68,
                'knockout_win_rate': 0.55,
                'penalty_shootout_skill': 0.61,

                # Match context
                'home_advantage': 0.00,
                'climate_similarity': 0.85,
                'travel_distance_km': 950,
                'rest_days': 4,

                # Stability
                'variance_index': 0.28,

                # Metadata
                'coach': 'José Peseiro',
                'key_player': 'Victor Osimhen',
                'style': 'Fast, attacking, physical',
                'weakness': 'Defensive consistency',
                'colors': {'primary': '#008751', 'secondary': '#FFFFFF'}  # Green & White
            },
            'Tanzania': {
                # Rankings & global strength
                'fifa_rank': 121,
                'elo': 1480,
                'team_strength_index': 0.48,

                # Attack & defense
                'attack_strength': 0.95,
                'defense_strength': 1.25,
                'attack_defense_ratio': 0.76,

                # Goals & expected goals
                'avg_goals': 0.95,
                'avg_conceded': 1.45,
                'xg_for': 1.05,
                'xg_against': 1.50,

                # Shooting & possession
                'shots_per_match': 8.7,
                'shots_on_target': 3.1,
                'possession': 41.8,
                'pass_accuracy': 76.4,

                # Recent form
                'form_last_5': [0, 0.5, 0, 1, 0.5],
                'goals_last_5': 4,
                'conceded_last_5': 8,
                'clean_sheets_last_5': 1,

                # Squad quality
                'squad_value_million_eur': 45,
                'avg_player_rating': 6.4,
                'players_top5_leagues': 2,
                'avg_age': 27.8,
                'injury_index': 0.22,
                'star_dependency': 0.45,

                # Tactical metrics
                'pressing_intensity': 0.42,
                'defensive_line_height': 0.35,
                'counter_attack_rate': 0.65,
                'set_piece_goals_ratio': 0.25,

                # Experience & psychology
                'coach_experience_years': 5,
                'squad_afcon_experience': 0.42,
                'knockout_win_rate': 0.28,
                'penalty_shootout_skill': 0.48,

                # Match context
                'home_advantage': 0.00,
                'climate_similarity': 0.82,
                'travel_distance_km': 1100,
                'rest_days': 5,

                # Stability
                'variance_index': 0.41,

                # Metadata
                'coach': 'Adel Amrouche',
                'key_player': 'Simon Msuva',
                'style': 'Defensive, disciplined, counter-attack',
                'weakness': 'Creativity in attack',
                'colors': {'primary': '#1EB53A', 'secondary': '#002664'}  # Green & Blue
            }
        }
    
    def calculate_team_metrics(self, team_data):
        """Calculate advanced metrics from team data"""
        metrics = team_data.copy()
        
        # Calculate recent form score (weighted average)
        form_weights = [0.35, 0.25, 0.20, 0.15, 0.05]
        form_score = np.dot(metrics['form_last_5'], form_weights) if len(metrics['form_last_5']) == 5 else 0.5
        
        # Goal conversion rates
        shot_efficiency = metrics['avg_goals'] / metrics['shots_per_match'] if metrics['shots_per_match'] > 0 else 0
        sot_efficiency = metrics['avg_goals'] / metrics['shots_on_target'] if metrics['shots_on_target'] > 0 else 0
        
        # xG performance
        xg_overperformance = metrics['avg_goals'] / metrics['xg_for'] if metrics['xg_for'] > 0 else 1.0
        xga_underperformance = metrics['xg_against'] / metrics['avg_conceded'] if metrics['avg_conceded'] > 0 else 1.0
        
        # Squad depth factor
        squad_depth = 1 - (metrics['injury_index'] * 0.5 + metrics['star_dependency'] * 0.3)
        
        # Tactical effectiveness
        tactical_score = (
            metrics['pressing_intensity'] * 0.25 +
            (1 - metrics['defensive_line_height']) * 0.25 +
            metrics['counter_attack_rate'] * 0.25 +
            metrics['set_piece_goals_ratio'] * 0.25
        )
        
        # Experience factor
        experience_factor = (
            min(metrics['coach_experience_years'] / 20, 1) * 0.3 +
            metrics['squad_afcon_experience'] * 0.4 +
            metrics['knockout_win_rate'] * 0.3
        )
        
        # Overall team quality index
        quality_index = (
            metrics['team_strength_index'] * 0.25 +
            (metrics['squad_value_million_eur'] / 400) * 0.20 +  # Nigeria has high value
            (metrics['avg_player_rating'] / 7.5) * 0.15 +
            (metrics['players_top5_leagues'] / 15) * 0.10 +
            form_score * 0.15 +
            tactical_score * 0.10 +
            experience_factor * 0.05
        )
        
        # Return enhanced metrics
        enhanced = {
            'team': metrics.get('coach', '').split()[-1],
            'form_score': form_score,
            'shot_efficiency': shot_efficiency,
            'sot_efficiency': sot_efficiency,
            'xg_overperformance': xg_overperformance,
            'xga_underperformance': xga_underperformance,
            'squad_depth': squad_depth,
            'tactical_score': tactical_score,
            'experience_factor': experience_factor,
            'quality_index': quality_index,
            'defensive_solidity': metrics['defense_strength'] * (1 - metrics['variance_index']),
            'attack_consistency': metrics['attack_strength'] * (1 - metrics['variance_index']),
            'momentum': np.mean(metrics['form_last_5'][-3:]) if len(metrics['form_last_5']) >= 3 else 0.5
        }
        
        # Add original data
        enhanced.update(metrics)
        
        return enhanced
    
    def get_match_context(self, home_team, away_team):
        """Get match context for Morocco 2025"""
        # Select venue (Casablanca for important matches)
        city = 'Casablanca'
        venue = self.VENUES[city]
        
        # Calculate team-specific advantages
        home_data = self.TEAMS[home_team]
        away_data = self.TEAMS[away_team]
        
        # Altitude adaptation
        altitude_factor_home = 1.0 - min(abs(venue['altitude'] - 400) / 1000, 0.1)
        altitude_factor_away = 1.0 - min(abs(venue['altitude'] - 300) / 1000, 0.1)
        
        # Climate similarity advantage
        climate_home = home_data['climate_similarity']
        climate_away = away_data['climate_similarity']
        
        # Travel fatigue
        travel_home = 1.0 - min(home_data['travel_distance_km'] / 5000, 0.1)
        travel_away = 1.0 - min(away_data['travel_distance_km'] / 5000, 0.1)
        
        # Rest advantage
        rest_home = 1.0 + (home_data['rest_days'] - 3) * 0.05
        rest_away = 1.0 + (away_data['rest_days'] - 3) * 0.05
        
        context = {
            'tournament': 'Africa Cup of Nations 2025',
            'host_country': 'Morocco',
            'host_city': city,
            'stadium': venue['stadium'],
            'capacity': venue['capacity'],
            'temperature': venue['temp'],
            'humidity': venue['humidity'],
            'altitude': venue['altitude'],
            'kickoff_time': '20:00 WET',
            'date': 'January 2025',
            'stage': 'Group Stage',
            'pitch_condition': 'Excellent',
            'expected_attendance': int(venue['capacity'] * 0.95),  # Nigeria draws big crowds
            
            # Team-specific advantages
            'home_advantages': {
                'altitude': altitude_factor_home,
                'climate': climate_home,
                'travel': travel_home,
                'rest': rest_home
            },
            'away_advantages': {
                'altitude': altitude_factor_away,
                'climate': climate_away,
                'travel': travel_away,
                'rest': rest_away
            },
            
            # Match dynamics
            'time_of_day': 'Prime Time',
            'weather_conditions': 'Cool evening, perfect conditions',
            'importance_coefficient': 0.85,
            'neutral_venue': True,
            'derby_factor': 0.0,
            'style_clash': 'Attacking flair vs Defensive discipline',
            'historical_context': 'Nigeria heavy favorites, Tanzania underdogs'
        }
        
        return context
    
    def calculate_expected_goals(self, home_metrics, away_metrics, context):
        """Calculate expected goals using advanced metrics"""
        
        # Base xG from team data
        lambda_home_base = home_metrics['xg_for']
        lambda_away_base = away_metrics['xg_for']
        
        # Adjust for opponent defense
        lambda_home_adjusted = lambda_home_base * away_metrics['defense_strength']
        lambda_away_adjusted = lambda_away_base * home_metrics['defense_strength']
        
        # Form adjustments
        home_form = home_metrics['form_score']
        away_form = away_metrics['form_score']
        form_adjustment = (home_form - away_form) * 0.35  # Increased weight for form
        
        # Quality difference (big gap here)
        quality_diff = home_metrics['quality_index'] - away_metrics['quality_index']
        
        # Squad depth impact
        depth_advantage = home_metrics['squad_depth'] - away_metrics['squad_depth']
        
        # Tactical matchup analysis
        tactical_advantage = self.analyze_tactical_matchup(home_metrics, away_metrics)
        
        # Experience advantage
        experience_advantage = home_metrics['experience_factor'] - away_metrics['experience_factor']
        
        # Contextual advantages
        home_context = np.mean(list(context['home_advantages'].values()))
        away_context = np.mean(list(context['away_advantages'].values()))
        context_advantage = home_context - away_context
        
        # Injury impact
        injury_impact_home = 1 - home_metrics['injury_index']
        injury_impact_away = 1 - away_metrics['injury_index']
        
        # Star player dependency
        star_impact_home = 1 - home_metrics['star_dependency'] * 0.25  # Nigeria less dependent on stars
        star_impact_away = 1 - away_metrics['star_dependency'] * 0.35  # Tanzania more dependent
        
        # Apply all adjustments with weighted importance
        lambda_home = lambda_home_adjusted * (
            1 + 
            form_adjustment * 0.25 +          # Form very important
            quality_diff * 0.35 +              # Big quality gap
            depth_advantage * 0.15 +
            tactical_advantage * 0.12 +
            experience_advantage * 0.08 +
            context_advantage * 0.05
        ) * injury_impact_home * star_impact_home
        
        lambda_away = lambda_away_adjusted * (
            1 - 
            form_adjustment * 0.20 +
            -quality_diff * 0.25 +            # Smaller negative impact for underdog
            -depth_advantage * 0.10 +
            -tactical_advantage * 0.10 +
            -experience_advantage * 0.05 +
            -context_advantage * 0.05
        ) * injury_impact_away * star_impact_away
        
        # Ensure realistic values
        lambda_home = max(0.3, min(3.5, lambda_home))
        lambda_away = max(0.1, min(2.5, lambda_away))
        
        # AFCON-specific adjustment
        lambda_home *= 0.92
        lambda_away *= 0.88
        
        # Store adjustments
        adjustments = {
            'base_home_xg': lambda_home_base,
            'base_away_xg': lambda_away_base,
            'form_adjustment': form_adjustment,
            'quality_difference': quality_diff,
            'tactical_advantage': tactical_advantage,
            'context_advantage': context_advantage,
            'depth_advantage': depth_advantage,
            'experience_advantage': experience_advantage,
            'injury_impact_home': injury_impact_home,
            'injury_impact_away': injury_impact_away,
            'star_impact_home': star_impact_home,
            'star_impact_away': star_impact_away
        }
        
        return lambda_home, lambda_away, adjustments
    
    def analyze_tactical_matchup(self, home_metrics, away_metrics):
        """Analyze tactical matchup between teams"""
        
        # Nigeria (attacking, fast) vs Tanzania (defensive, counter)
        if home_metrics['style'] == 'Fast, attacking, physical' and away_metrics['style'] == 'Defensive, disciplined, counter-attack':
            # Nigeria's attack vs Tanzania's defense
            nigeria_advantage = (
                home_metrics['attack_strength'] * 0.4 -
                away_metrics['defense_strength'] * 0.3 +
                home_metrics['pressing_intensity'] * 0.2 -
                away_metrics['counter_attack_rate'] * 0.1
            )
        else:
            # Generic tactical advantage
            nigeria_advantage = home_metrics['tactical_score'] - away_metrics['tactical_score']
        
        return nigeria_advantage * 0.6
    
    def bivariate_poisson_probabilities(self, lambda_home, lambda_away, max_goals=6):
        """Calculate probabilities using bivariate Poisson"""
        
        # Correlation parameter for mismatch games
        rho = -0.08  # Less correlation in one-sided matches
        
        probs = np.zeros((max_goals + 1, max_goals + 1))
        
        for i in range(max_goals + 1):
            for j in range(max_goals + 1):
                # Independent Poisson
                indep_prob = (
                    stats.poisson.pmf(i, lambda_home) *
                    stats.poisson.pmf(j, lambda_away)
                )
                
                # Bivariate adjustment
                bv_factor = 1.0
                if i == 0 and j == 0:
                    bv_factor = 1 - (lambda_home * lambda_away * rho)
                elif i == 0 and j == 1:
                    bv_factor = 1 + (lambda_home * rho)
                elif i == 1 and j == 0:
                    bv_factor = 1 + (lambda_away * rho)
                elif i == 1 and j == 1:
                    bv_factor = 1 - rho
                
                # AFCON-specific adjustments (less for mismatch)
                afcon_factor = 1.0
                if i == j:  # Draws less likely in mismatch
                    afcon_factor = 0.9 if i > 0 else 1.1  # 0-0 still possible
                elif i == 0 and j > 0:  # Tanzania scoring
                    afcon_factor = 1.05  # Slight boost for underdog
                
                probs[i, j] = indep_prob * bv_factor * afcon_factor
        
        # Normalize
        probs = probs / probs.sum()
        
        return probs
    
    def predict_exact_score(self, home_team='Nigeria', away_team='Tanzania'):
        """Main prediction function"""
        print(f"\n{'='*100}")
        print(f"🏆 AFCON 2025: {home_team} vs {away_team} - EXACT SCORE PREDICTION")
        print(f"{'='*100}")
        
        # Get team metrics
        home_metrics = self.calculate_team_metrics(self.TEAMS[home_team])
        away_metrics = self.calculate_team_metrics(self.TEAMS[away_team])
        
        # Get match context
        context = self.get_match_context(home_team, away_team)
        
        # Display header
        print(f"\n📍 Venue: {context['stadium']}, {context['host_city']}, Morocco")
        print(f"📅 Date: {context['date']} | ⏰ Time: {context['kickoff_time']}")
        print(f"🌡️ Conditions: {context['temperature']}°C, {context['humidity']}% humidity")
        print(f"🎯 Match Context: {context['historical_context']}")
        print(f"{'='*100}")
        
        # Display team comparison
        self.display_team_comparison(home_metrics, away_metrics)
        
        # Calculate expected goals
        print("\n🤖 Calculating advanced prediction...")
        lambda_home, lambda_away, adjustments = self.calculate_expected_goals(
            home_metrics, away_metrics, context
        )
        
        # Get probability matrix
        probs = self.bivariate_poisson_probabilities(lambda_home, lambda_away)
        
        # Get results
        max_idx = np.unravel_index(np.argmax(probs), probs.shape)
        predicted_score = f"{max_idx[0]}-{max_idx[1]}"
        confidence = probs[max_idx] * 100
        
        # Calculate outcome probabilities
        home_win = np.sum(np.triu(probs, k=1))
        draw = np.sum(np.diag(probs))
        away_win = np.sum(np.tril(probs, k=-1))
        
        # Get top scores
        flat_indices = np.argsort(probs.flatten())[::-1][:15]
        top_scores = []
        for idx in flat_indices:
            h_goals, a_goals = np.unravel_index(idx, probs.shape)
            top_scores.append({
                'score': f"{h_goals}-{a_goals}",
                'probability': probs[h_goals, a_goals] * 100
            })
        
        # Display results
        self.display_prediction_results(
            home_team, away_team,
            predicted_score, confidence,
            lambda_home, lambda_away,
            home_win, draw, away_win,
            top_scores, home_metrics, away_metrics,
            context, adjustments
        )
        
        # Create visualization
        self.create_prediction_visualization(
            home_team, away_team, context,
            probs, predicted_score, confidence,
            lambda_home, lambda_away,
            home_win, draw, away_win,
            top_scores, home_metrics, away_metrics
        )
        
        # Return results
        result = self.compile_results(
            home_team, away_team, context,
            predicted_score, confidence,
            lambda_home, lambda_away,
            home_win, draw, away_win,
            top_scores, probs, home_metrics, away_metrics, adjustments
        )
        
        return result
    
    def display_team_comparison(self, home_metrics, away_metrics):
        """Display detailed team comparison"""
        print(f"\n📊 TEAM ANALYSIS & COMPARISON")
        print(f"{'='*100}")
        
        # Head-to-head comparison
        comparisons = [
            ('FIFA Ranking', f"#{home_metrics['fifa_rank']}", f"#{away_metrics['fifa_rank']}"),
            ('Elo Rating', f"{home_metrics['elo']}", f"{away_metrics['elo']}"),
            ('Squad Value', f"€{home_metrics['squad_value_million_eur']}M", f"€{away_metrics['squad_value_million_eur']}M"),
            ('Attack Strength', f"{home_metrics['attack_strength']:.2f}", f"{away_metrics['attack_strength']:.2f}"),
            ('Defense Strength', f"{home_metrics['defense_strength']:.2f}", f"{away_metrics['defense_strength']:.2f}"),
            ('Avg Goals', f"{home_metrics['avg_goals']:.2f}", f"{away_metrics['avg_goals']:.2f}"),
            ('Avg Conceded', f"{home_metrics['avg_conceded']:.2f}", f"{away_metrics['avg_conceded']:.2f}"),
            ('Shots/Match', f"{home_metrics['shots_per_match']:.1f}", f"{away_metrics['shots_per_match']:.1f}"),
            ('Possession %', f"{home_metrics['possession']:.1f}%", f"{away_metrics['possession']:.1f}%"),
            ('Top 5 League Players', f"{home_metrics['players_top5_leagues']}", f"{away_metrics['players_top5_leagues']}"),
            ('Recent Form', f"{home_metrics['form_score']:.2f}", f"{away_metrics['form_score']:.2f}"),
            ('AFCON Experience', f"{home_metrics['squad_afcon_experience']:.2f}", f"{away_metrics['squad_afcon_experience']:.2f}")
        ]
        
        print(f"\n{'Metric':<25} {'Nigeria':<15} {'Tanzania':<15} {'Advantage':<12} {'Ratio':<8}")
        print(f"{'-'*25}{'-'*15}{'-'*15}{'-'*12}{'-'*8}")
        
        for category, nig_val, tan_val in comparisons:
            # Calculate advantage and ratio
            try:
                if '#' in nig_val:
                    nig_num = int(nig_val[1:])
                    tan_num = int(tan_val[1:])
                    advantage = "Nigeria" if nig_num < tan_num else "Tanzania" if nig_num > tan_num else "Equal"
                    ratio = f"{min(nig_num, tan_num)/max(nig_num, tan_num):.2f}" if nig_num != tan_num else "1.00"
                elif '€' in nig_val:
                    nig_num = float(''.join(c for c in nig_val if c.isdigit() or c == '.'))
                    tan_num = float(''.join(c for c in tan_val if c.isdigit() or c == '.'))
                    advantage = "Nigeria" if nig_num > tan_num else "Tanzania" if nig_num < tan_num else "Equal"
                    ratio = f"{max(nig_num, tan_num)/min(nig_num, tan_num):.1f}x" if min(nig_num, tan_num) > 0 else "N/A"
                else:
                    nig_num = float(''.join(c for c in nig_val if c.isdigit() or c == '.'))
                    tan_num = float(''.join(c for c in tan_val if c.isdigit() or c == '.'))
                    advantage = "Nigeria" if nig_num > tan_num else "Tanzania" if nig_num < tan_num else "Equal"
                    ratio = f"{max(nig_num, tan_num)/min(nig_num, tan_num):.2f}" if min(nig_num, tan_num) > 0 else "N/A"
            except:
                advantage = "-"
                ratio = "-"
            
            print(f"{category:<25} {nig_val:<15} {tan_val:<15} {advantage:<12} {ratio:<8}")
        
        # Key insights
        print(f"\n🔑 KEY INSIGHTS:")
        print(f"   • Nigeria has {home_metrics['squad_value_million_eur']/away_metrics['squad_value_million_eur']:.1f}x higher squad value")
        print(f"   • Nigeria creates {home_metrics['shots_per_match']/away_metrics['shots_per_match']:.1f}x more shots per game")
        print(f"   • Nigeria has {home_metrics['players_top5_leagues']/max(away_metrics['players_top5_leagues'], 1):.1f}x more top league players")
        print(f"   • Tanzania's defense is {away_metrics['defense_strength']/home_metrics['defense_strength']:.1f}x more organized")
        print(f"   • Form advantage: Nigeria {home_metrics['form_score']:.2f} vs Tanzania {away_metrics['form_score']:.2f}")
        
        print(f"\n🎯 TACTICAL PREVIEW:")
        print(f"   • Nigeria will: {home_metrics['style']}")
        print(f"   • Tanzania will: {away_metrics['style']}")
        print(f"   • Key matchup: {home_metrics['key_player']} (Nigeria) vs {away_metrics['key_player']} (Tanzania)")
        print(f"   • Coaches: {home_metrics['coach']} vs {away_metrics['coach']}")
    
    def display_prediction_results(self, home_team, away_team, predicted_score, confidence,
                                 lambda_home, lambda_away, home_win, draw, away_win,
                                 top_scores, home_metrics, away_metrics, context, adjustments):
        """Display prediction results"""
        print(f"\n{'='*100}")
        print("🎯 PREDICTION RESULTS")
        print(f"{'='*100}")
        
        print(f"\n🏆 MOST LIKELY EXACT SCORE: {predicted_score}")
        print(f"   📊 Model Confidence: {confidence:.1f}%")
        
        print(f"\n⚽ EXPECTED GOALS ANALYSIS:")
        print(f"   {home_team}: {lambda_home:.2f} (Base xG: {adjustments['base_home_xg']:.2f}, +{(lambda_home/adjustments['base_home_xg']-1)*100:.1f}% adjustment)")
        print(f"   {away_team}: {lambda_away:.2f} (Base xG: {adjustments['base_away_xg']:.2f}, +{(lambda_away/adjustments['base_away_xg']-1)*100:.1f}% adjustment)")
        
        print(f"\n📈 MATCH OUTCOME PROBABILITIES:")
        print(f"   {home_team} Win: {home_win*100:.1f}%")
        print(f"   Draw: {draw*100:.1f}%")
        print(f"   {away_team} Win: {away_win*100:.1f}%")
        
        print(f"\n🔝 TOP 10 MOST PROBABLE SCORES:")
        print(f"{'-'*60}")
        print(f"   Rank  Score      Probability   Cumulative   Expected Occurrence")
        print(f"{'-'*60}")
        
        cum_prob = 0
        for i, score in enumerate(top_scores[:10], 1):
            cum_prob += score['probability']
            expected = int(100 / score['probability']) if score['probability'] > 0 else 999
            print(f"   {i:2d}.  {score['score']:^8}     {score['probability']:5.1f}%       {cum_prob:5.1f}%       1 in {expected:3d}")
        
        print(f"\n📊 STATISTICAL ANALYSIS:")
        print(f"   • Nigeria clean sheet probability: {np.sum(probs[:, 0])*100:.1f}%")
        print(f"   • Tanzania clean sheet probability: {np.sum(probs[0, :])*100:.1f}%")
        print(f"   • Over 1.5 goals probability: {(1 - probs[0:2, 0:2].sum())*100:.1f}%")
        print(f"   • Over 2.5 goals probability: {(1 - probs[0:3, 0:3].sum())*100:.1f}%")
        print(f"   • Both teams to score: {(1 - probs[:, 0].sum() - probs[0, :].sum() + probs[0, 0])*100:.1f}%")
        
        print(f"\n💡 KEY PREDICTION FACTORS:")
        print(f"   1. Quality Gap: Nigeria +{(adjustments['quality_difference']*100):.1f}% advantage")
        print(f"   2. Form Difference: Nigeria +{(adjustments['form_adjustment']*100):.1f}%")
        print(f"   3. Squad Value: Nigeria {home_metrics['squad_value_million_eur']/away_metrics['squad_value_million_eur']:.1f}x higher")
        print(f"   4. Attack vs Defense: Nigeria attack {home_metrics['attack_strength']:.2f} vs Tanzania defense {away_metrics['defense_strength']:.2f}")
        print(f"   5. Experience: Nigeria +{(adjustments['experience_advantage']*100):.1f}%")
        print(f"   6. Tactical: {'Nigeria' if adjustments['tactical_advantage'] > 0 else 'Tanzania'} +{(abs(adjustments['tactical_advantage'])*100):.1f}%")
        
        print(f"\n🎯 MATCH PREDICTION SUMMARY:")
        if home_win > 0.6:
            print(f"   • Nigeria are STRONG FAVORITES to win this match")
            print(f"   • Most likely scenario: Nigeria wins by 1-2 goals")
            print(f"   • Key: Early Nigeria goal could open up the match")
        elif home_win > 0.45:
            print(f"   • Nigeria are FAVORITES but Tanzania can make it difficult")
            print(f"   • Most likely: Close Nigeria win or draw")
            print(f"   • Key: Tanzania's defensive organization")
        else:
            print(f"   • This is a COMPETITIVE match with no clear favorite")
            print(f"   • Most likely: Draw or narrow victory either way")
        
        print(f"\n📍 CONTEXT:")
        print(f"   • Venue: {context['stadium']} (Neutral)")
        print(f"   • Stage: {context['stage']} - High importance for both")
        print(f"   • Conditions: Ideal football weather")
        print(f"   • Crowd: Expected {context['expected_attendance']:,} (mostly neutral)")
        
        print(f"\n📝 MODEL NOTES:")
        print(f"   • Using Bivariate Poisson with AFCON 2025 parameters")
        print(f"   • Accounts for Nigeria's attacking power vs Tanzania's defensive setup")
        print(f"   • Includes underdog motivation factor for Tanzania")
        print(f"   • Weighted for tournament context and match importance")
        
        print(f"\n{'='*100}")
    
    def create_prediction_visualization(self, home_team, away_team, context,
                                       probs, predicted_score, confidence,
                                       lambda_home, lambda_away,
                                       home_win, draw, away_win,
                                       top_scores, home_metrics, away_metrics):
        """Create comprehensive visualization"""
        
        fig = plt.figure(figsize=(24, 16))
        
        # Get team colors
        home_color = home_metrics['colors']['primary']
        away_color = away_metrics['colors']['primary']
        
        # Create grid
        gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        
        # 1. Main title
        ax_title = fig.add_subplot(gs[0, :])
        ax_title.axis('off')
        title_text = (
            f"AFCON 2025 MOROCCO: {home_team} vs {away_team}\n"
            f"EXACT SCORE PREDICTION - ADVANCED ANALYTICS MODEL\n"
            f"📍 {context['stadium']}, {context['host_city']} | 📅 {context['date']} | ⏰ {context['kickoff_time']} | 🌡️ {context['temperature']}°C"
        )
        ax_title.text(0.5, 0.7, title_text, ha='center', va='center', 
                     fontsize=22, fontweight='bold')
        pred_text = f"PREDICTED SCORE: {predicted_score} (Confidence: {confidence:.1f}%)"
        ax_title.text(0.5, 0.3, pred_text, ha='center', va='center', 
                     fontsize=18, color='darkred', fontweight='bold')
        
        # 2. Score Probability Heatmap
        ax1 = fig.add_subplot(gs[1, :2])
        mask = np.zeros_like(probs)
        mask[np.triu_indices_from(mask, k=1)] = True
        
        sns.heatmap(
            probs * 100,
            annot=True,
            fmt='.1f',
            cmap='RdYlGn',
            ax=ax1,
            mask=mask,
            cbar_kws={'label': 'Probability (%)', 'shrink': 0.8},
            linewidths=1,
            linecolor='gray',
            annot_kws={'size': 8, 'weight': 'bold'}
        )
        
        pred_home, pred_away = map(int, predicted_score.split('-'))
        ax1.add_patch(plt.Rectangle(
            (pred_away, pred_home), 1, 1,
            fill=False, edgecolor='blue', lw=3, linestyle='--'
        ))
        
        ax1.set_xlabel(f'{away_team} Goals', fontsize=12, fontweight='bold')
        ax1.set_ylabel(f'{home_team} Goals', fontsize=12, fontweight='bold')
        ax1.set_title('Exact Score Probability Matrix (%)', fontsize=14, fontweight='bold')
        ax1.invert_yaxis()
        
        # 3. Top Scores Bar Chart
        ax2 = fig.add_subplot(gs[1, 2])
        scores = [s['score'] for s in top_scores[:8]]
        score_probs = [s['probability'] for s in top_scores[:8]]
        
        bars = ax2.barh(scores[::-1], score_probs[::-1], color='steelblue', edgecolor='navy', alpha=0.7)
        ax2.set_xlabel('Probability (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Top 8 Most Probable Scores', fontsize=14, fontweight='bold')
        ax2.set_xlim(0, max(score_probs) * 1.3)
        
        for i, (bar, prob) in enumerate(zip(bars, score_probs[::-1])):
            width = bar.get_width()
            ax2.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                    f'{prob:.1f}%', ha='left', va='center', fontsize=10)
        
        # 4. Outcome Probabilities
        ax3 = fig.add_subplot(gs[1, 3])
        outcomes = [f'{home_team}\nWin', 'Draw', f'{away_team}\nWin']
        outcome_probs = [home_win * 100, draw * 100, away_win * 100]
        colors = [home_color, '#808080', away_color]
        
        bars = ax3.bar(outcomes, outcome_probs, color=colors, edgecolor='black', alpha=0.8)
        ax3.set_ylabel('Probability (%)', fontsize=12, fontweight='bold')
        ax3.set_title('Match Outcome Probabilities', fontsize=14, fontweight='bold')
        ax3.set_ylim(0, max(outcome_probs) * 1.4)
        
        for bar, prob in zip(bars, outcome_probs):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{prob:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # 5. Expected Goals Comparison
        ax4 = fig.add_subplot(gs[2, 0])
        teams = [home_team, away_team]
        xg_values = [lambda_home, lambda_away]
        colors_xg = [home_color, away_color]
        
        bars = ax4.bar(teams, xg_values, color=colors_xg, edgecolor='black', alpha=0.7)
        ax4.set_ylabel('Expected Goals (xG)', fontsize=12, fontweight='bold')
        ax4.set_title('Expected Goals Comparison', fontsize=14, fontweight='bold')
        ax4.set_ylim(0, max(xg_values) * 1.5)
        
        for bar, xg in zip(bars, xg_values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{xg:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 6. Team Strength Radar Chart
        ax5 = fig.add_subplot(gs[2, 1], projection='polar')
        
        categories = ['Attack', 'Defense', 'Squad\nValue', 'Form', 'Experience', 'Tactics']
        N = len(categories)
        
        home_values = [
            home_metrics['attack_strength'] / 2,
            home_metrics['defense_strength'] / 2,
            home_metrics['squad_value_million_eur'] / 500,
            home_metrics['form_score'],
            home_metrics['experience_factor'],
            home_metrics['tactical_score']
        ]
        
        away_values = [
            away_metrics['attack_strength'] / 2,
            away_metrics['defense_strength'] / 2,
            away_metrics['squad_value_million_eur'] / 500,
            away_metrics['form_score'],
            away_metrics['experience_factor'],
            away_metrics['tactical_score']
        ]
        
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        angles += angles[:1]
        
        home_values += home_values[:1]
        away_values += away_values[:1]
        
        ax5.plot(angles, home_values, 'o-', linewidth=2, label=home_team, color=home_color)
        ax5.fill(angles, home_values, alpha=0.25, color=home_color)
        ax5.plot(angles, away_values, 'o-', linewidth=2, label=away_team, color=away_color)
        ax5.fill(angles, away_values, alpha=0.25, color=away_color)
        
        ax5.set_xticks(angles[:-1])
        ax5.set_xticklabels(categories)
        ax5.set_ylim(0, 1)
        ax5.set_title('Team Strength Comparison', fontsize=14, fontweight='bold')
        ax5.legend(loc='upper right')
        
        # 7. Score Distribution
        ax6 = fig.add_subplot(gs[2, 2])
        
        low_scoring = probs[0:2, 0:2].sum() * 100
        medium_scoring = (probs[2:4, 2:4].sum() + probs[0:2, 2:4].sum() + probs[2:4, 0:2].sum()) * 100
        high_scoring = (probs[4:, :].sum() + probs[:, 4:].sum()) * 100
        
        categories_dist = ['Low (0-1)', 'Medium (2-3)', 'High (4+)']
        dist_values = [low_scoring, medium_scoring, high_scoring]
        colors_dist = ['lightgreen', 'gold', 'lightcoral']
        
        bars = ax6.bar(categories_dist, dist_values, color=colors_dist, edgecolor='black', alpha=0.7)
        ax6.set_ylabel('Probability (%)', fontsize=12, fontweight='bold')
        ax6.set_title('Score Distribution Analysis', fontsize=14, fontweight='bold')
        ax6.set_ylim(0, max(dist_values) * 1.4)
        
        for bar, val in zip(bars, dist_values):
            height = bar.get_height()
            ax6.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{val:.1f}%', ha='center', va='bottom')
        
        # 8. Key Metrics Comparison
        ax7 = fig.add_subplot(gs[2, 3])
        ax7.axis('off')
        
        metrics_text = (
            f"KEY METRICS COMPARISON\n"
            f"{'='*40}\n\n"
            f"{home_team.upper()}:\n"
            f"• FIFA: #{home_metrics['fifa_rank']}\n"
            f"• Squad: €{home_metrics['squad_value_million_eur']}M\n"
            f"• Attack: {home_metrics['attack_strength']:.2f}\n"
            f"• Goals: {home_metrics['avg_goals']:.2f}/match\n"
            f"• Shots: {home_metrics['shots_per_match']:.1f}/match\n"
            f"• Form: {home_metrics['form_score']:.2f}\n\n"
            f"{away_team.upper()}:\n"
            f"• FIFA: #{away_metrics['fifa_rank']}\n"
            f"• Squad: €{away_metrics['squad_value_million_eur']}M\n"
            f"• Defense: {away_metrics['defense_strength']:.2f}\n"
            f"• Conceded: {away_metrics['avg_conceded']:.2f}/match\n"
            f"• Possession: {away_metrics['possession']:.1f}%\n"
            f"• Form: {away_metrics['form_score']:.2f}"
        )
        
        ax7.text(0.05, 0.95, metrics_text, transform=ax7.transAxes,
                fontsize=10, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
        
        # 9. Tactical Analysis
        ax8 = fig.add_subplot(gs[3, 0])
        ax8.axis('off')
        
        tactical_text = (
            f"TACTICAL ANALYSIS\n"
            f"{'='*40}\n\n"
            f"{home_team.upper()}:\n"
            f"• Style: {home_metrics['style']}\n"
            f"• Key: {home_metrics['key_player']}\n"
            f"• Coach: {home_metrics['coach']}\n"
            f"• Strength: Pace, power, attack\n"
            f"• Weakness: {home_metrics['weakness']}\n\n"
            f"{away_team.upper()}:\n"
            f"• Style: {away_metrics['style']}\n"
            f"• Key: {away_metrics['key_player']}\n"
            f"• Coach: {away_metrics['coach']}\n"
            f"• Strength: Defense, discipline\n"
            f"• Weakness: {away_metrics['weakness']}"
        )
        
        ax8.text(0.05, 0.95, tactical_text, transform=ax8.transAxes,
                fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        # 10. Prediction Insights
        ax9 = fig.add_subplot(gs[3, 1])
        ax9.axis('off')
        
        insights_text = (
            f"PREDICTION INSIGHTS\n"
            f"{'='*40}\n\n"
            f"✅ Favoring {home_team}:\n"
            f"• 8.4x higher squad value\n"
            f"• 1.5x better attack\n"
            f"• Much better recent form\n"
            f"• More experienced squad\n"
            f"• Superior individual quality\n\n"
            f"✅ Favoring {away_team}:\n"
            f"• Defensive organization\n"
            f"• Nothing to lose attitude\n"
            f"• Potential for counter-attacks\n"
            f"• Underdog motivation"
        )
        
        ax9.text(0.05, 0.95, insights_text, transform=ax9.transAxes,
                fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
        
        # 11. Match Context
        ax10 = fig.add_subplot(gs[3, 2])
        ax10.axis('off')
        
        context_text = (
            f"MATCH CONTEXT\n"
            f"{'='*40}\n\n"
            f"🏆 Tournament: AFCON 2025\n"
            f"📍 Host: Morocco\n"
            f"🏟️ Venue: {context['stadium']}\n"
            f"🌡️ Temp: {context['temperature']}°C\n"
            f"💧 Humidity: {context['humidity']}%\n"
            f"⏰ Time: {context['time_of_day']}\n"
            f"🎯 Stage: {context['stage']}\n"
            f"👥 Attendance: {context['expected_attendance']:,}\n"
            f"⚖️ Importance: {context['importance_coefficient']*100:.0f}%"
        )
        
        ax10.text(0.05, 0.95, context_text, transform=ax10.transAxes,
                fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # 12. Final Prediction
        ax11 = fig.add_subplot(gs[3, 3])
        ax11.axis('off')
        
        final_text = (
            f"FINAL PREDICTION\n"
            f"{'='*40}\n\n"
            f"🎯 Exact Score:\n"
            f"   {predicted_score}\n"
            f"   Confidence: {confidence:.1f}%\n\n"
            f"⚽ Expected:\n"
            f"   {home_team}: {lambda_home:.2f}\n"
            f"   {away_team}: {lambda_away:.2f}\n\n"
            f"📈 Most Likely:\n"
            f"   1. {home_team} Win: {home_win*100:.1f}%\n"
            f"   2. Draw: {draw*100:.1f}%\n"
            f"   3. {away_team} Win: {away_win*100:.1f}%\n\n"
            f"💡 Verdict:\n"
            f"   Nigeria should win,\n"
            f"   but Tanzania will\n"
            f"   make it difficult"
        )
        
        ax11.text(0.05, 0.95, final_text, transform=ax11.transAxes,
                fontsize=10, verticalalignment='top', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='gold', alpha=0.7))
        
        # Footer
        plt.figtext(0.5, 0.02, 
                   f'AFCON 2025 PREDICTION MODEL | NIGERIA VS TANZANIA | {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                   ha='center', fontsize=11, style='italic',
                   bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))
        
        plt.tight_layout()
        
        # Save
        filename = f"AFCON2025_{home_team.replace(' ', '_')}_vs_{away_team.replace(' ', '_')}_Prediction.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"\n💾 Visualization saved: {filename}")
        
        plt.show()
    
    def compile_results(self, home_team, away_team, context, predicted_score, confidence,
                       lambda_home, lambda_away, home_win, draw, away_win,
                       top_scores, probs, home_metrics, away_metrics, adjustments):
        """Compile all results"""
        
        return {
            'match_info': {
                'home': home_team,
                'away': away_team,
                'venue': f"{context['stadium']}, {context['host_city']}, Morocco",
                'date': context['date'],
                'time': context['kickoff_time'],
                'stage': context['stage'],
                'temperature': context['temperature'],
                'humidity': context['humidity'],
                'attendance': context['expected_attendance'],
                'importance': context['importance_coefficient']
            },
            'prediction': {
                'exact_score': predicted_score,
                'confidence': round(confidence, 1),
                'expected_goals': {
                    'home': round(lambda_home, 2),
                    'away': round(lambda_away, 2)
                },
                'outcome_probabilities': {
                    'home_win': round(home_win * 100, 1),
                    'draw': round(draw * 100, 1),
                    'away_win': round(away_win * 100, 1)
                },
                'top_scores': top_scores[:10],
                'score_matrix_dimensions': probs.shape
            },
            'team_analysis': {
                'home': {
                    'fifa_rank': home_metrics['fifa_rank'],
                    'elo': home_metrics['elo'],
                    'squad_value': home_metrics['squad_value_million_eur'],
                    'attack_strength': round(home_metrics['attack_strength'], 2),
                    'defense_strength': round(home_metrics['defense_strength'], 2),
                    'avg_goals': round(home_metrics['avg_goals'], 2),
                    'form_score': round(home_metrics['form_score'], 3),
                    'quality_index': round(home_metrics['quality_index'], 3),
                    'coach': home_metrics['coach'],
                    'key_player': home_metrics['key_player']
                },
                'away': {
                    'fifa_rank': away_metrics['fifa_rank'],
                    'elo': away_metrics['elo'],
                    'squad_value': away_metrics['squad_value_million_eur'],
                    'attack_strength': round(away_metrics['attack_strength'], 2),
                    'defense_strength': round(away_metrics['defense_strength'], 2),
                    'avg_goals': round(away_metrics['avg_goals'], 2),
                    'form_score': round(away_metrics['form_score'], 3),
                    'quality_index': round(away_metrics['quality_index'], 3),
                    'coach': away_metrics['coach'],
                    'key_player': away_metrics['key_player']
                }
            },
            'key_ratios': {
                'squad_value_ratio': home_metrics['squad_value_million_eur'] / away_metrics['squad_value_million_eur'],
                'attack_ratio': home_metrics['attack_strength'] / away_metrics['attack_strength'],
                'defense_ratio': away_metrics['defense_strength'] / home_metrics['defense_strength'],
                'form_ratio': home_metrics['form_score'] / away_metrics['form_score']
            },
            'model_info': {
                'name': 'Advanced Bivariate Poisson Model',
                'version': 'AFCON 2025 v2.1',
                'timestamp': datetime.now().isoformat(),
                'parameters': {
                    'avg_goals_afcon': self.AVG_GOALS_AFCON,
                    'correlation_rho': -0.08,
                    'low_scoring_boost': self.LOW_SCORING_BOOST
                }
            }
        }


def main():
    """Main function"""
    
    print("\n" + "="*100)
    print("🏆 AFCON 2025: NIGERIA vs TANZANIA - EXACT SCORE PREDICTION")
    print("="*100)
    print("Advanced analytics model predicting the exact scoreline")
    print("Using detailed team metrics and bivariate Poisson distribution")
    print("="*100)
    
    # Create predictor
    predictor = AFCON2025Predictor()
    
    try:
        # Run prediction
        result = predictor.predict_exact_score('Nigeria', 'Tanzania')
        
        # Save results
        filename = "AFCON2025_Nigeria_vs_Tanzania_Prediction.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"\n💾 Complete prediction data saved: {filename}")
        
        # Display summary
        print(f"\n{'='*100}")
        print("📋 PREDICTION SUMMARY")
        print(f"{'='*100}")
        
        pred = result['prediction']
        teams = result['team_analysis']
        
        print(f"\n🎯 Exact Score: {pred['exact_score']} (Confidence: {pred['confidence']}%)")
        print(f"⚽ Expected Goals: Nigeria {pred['expected_goals']['home']:.2f} - Tanzania {pred['expected_goals']['away']:.2f}")
        
        outcomes = pred['outcome_probabilities']
        print(f"📈 Outcomes: Nigeria {outcomes['home_win']}% | Draw {outcomes['draw']}% | Tanzania {outcomes['away_win']}%")
        
        print(f"\n🔝 Top 3 Scores:")
        for i, score in enumerate(pred['top_scores'][:3], 1):
            print(f"   {i}. {score['score']}: {score['probability']:.1f}%")
        
        print(f"\n📊 Key Statistics:")
        print(f"   • Squad Value: Nigeria €{teams['home']['squad_value']}M vs Tanzania €{teams['away']['squad_value']}M")
        print(f"   • Ratio: {teams['home']['squad_value']/teams['away']['squad_value']:.1f}x in favor of Nigeria")
        print(f"   • FIFA Rank: #{teams['home']['fifa_rank']} vs #{teams['away']['fifa_rank']}")
        print(f"   • Attack: Nigeria {teams['home']['attack_strength']} vs Tanzania {teams['away']['attack_strength']}")
        
        print(f"\n✅ Prediction complete! Check the generated files.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Check dependencies
    try:
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        from scipy import stats
        import json
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("\nPlease install required packages:")
        print("pip install numpy pandas matplotlib seaborn scipy")
        exit(1)
    
    # Run prediction
    main()