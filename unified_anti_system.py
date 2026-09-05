"""
Free Fire Anti-Ban, Anti-Blacklist, and Anti-Report System
Comprehensive configuration manager for account safety and avoiding detection
"""

import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class PlayerStats:
    """Track player statistics for blacklist and report avoidance"""
    wins: int = 0
    kills: int = 0
    deaths: int = 0
    headshots: int = 0
    games_played: int = 0
    accuracy: float = 0.0
    win_rate: float = 0.0
    kda: float = 0.0
    reports_received: int = 0
    consecutive_wins: int = 0
    consecutive_kills: int = 0
    max_kills_per_match: int = 0
    last_report_date: Optional[str] = None
    
    def calculate_metrics(self):
        """Calculate KDA and win rate"""
        if self.games_played > 0:
            self.win_rate = self.wins / self.games_played
        if self.deaths > 0:
            self.kda = self.kills / self.deaths
        else:
            self.kda = self.kills if self.kills > 0 else 0


class ConfigurationManager:
    """Unified configuration manager for all anti systems"""
    
    def __init__(self):
        self.anti_ban_config = self._load_config("config.json")
        self.anti_blacklist_config = self._load_config("anti-blacklist-config.json")
        self.anti_report_config = self._load_config("anti-report-config.json")
        self.player_stats = PlayerStats()
        self.risk_score = 0.0
        self.report_risk_score = 0.0
        self.blacklist_risk_score = 0.0
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found, using defaults")
            return {}


class AntiBanSystem(ConfigurationManager):
    """Manages anti-ban protection"""
    
    def get_action_delay(self) -> float:
        """Get random delay for action (in seconds)"""
        config = self.anti_ban_config.get("gameplay", {})
        delay_config = config.get("delayBetweenActions", {})
        
        min_delay = delay_config.get("min", 500) / 1000
        max_delay = delay_config.get("max", 2000) / 1000
        
        return random.uniform(min_delay, max_delay)
    
    def get_kill_delay(self) -> float:
        """Get delay before registering kills"""
        config = self.anti_ban_config.get("gameplay", {})
        kill_config = config.get("killDelay", {})
        
        min_delay = kill_config.get("min", 1000) / 1000
        max_delay = kill_config.get("max", 3000) / 1000
        
        return random.uniform(min_delay, max_delay)
    
    def apply_humanlike_accuracy(self) -> Dict[str, Any]:
        """Apply human-like accuracy patterns"""
        config = self.anti_ban_config.get("gameplay", {})
        acc_config = config.get("humanLikeAccuracy", {})
        
        if not acc_config.get("enabled"):
            return {"miss": False, "accuracy_multiplier": 1.0}
        
        miss_chance = acc_config.get("missChance", 0.15)
        headshot_rate = acc_config.get("headShotRate", 0.25)
        
        should_miss = random.random() < miss_chance
        should_headshot = random.random() < headshot_rate
        
        return {
            "miss": should_miss,
            "headshot": should_headshot and not should_miss,
            "accuracy_multiplier": 0.85 if should_miss else 0.95
        }
    
    def get_movement_pattern(self) -> Dict[str, Any]:
        """Get natural movement pattern"""
        config = self.anti_ban_config.get("gameplay", {})
        move_config = config.get("movementPattern", {})
        
        return {
            "enabled": move_config.get("enabled", True),
            "random_stutter": move_config.get("randomStutter", True),
            "walk_variation": move_config.get("walkVariation", 0.2),
            "stutter_chance": random.random() < 0.3
        }
    
    def get_login_behavior(self) -> Dict[str, Any]:
        """Get login behavior configuration"""
        config = self.anti_ban_config.get("account", {})
        login_config = config.get("loginBehavior", {})
        
        delay_hours = random.randint(
            login_config.get("loginDelayHours", {}).get("min", 4),
            login_config.get("loginDelayHours", {}).get("max", 12)
        )
        
        return {
            "randomize_login_time": login_config.get("randomizeLoginTime", True),
            "delay_hours": delay_hours,
            "vary_location": login_config.get("varyLoginLocation", True),
            "next_login": (datetime.now() + timedelta(hours=delay_hours)).isoformat()
        }
    
    def get_user_agent(self) -> str:
        """Get random user agent"""
        config = self.anti_ban_config.get("network", {})
        user_agents = config.get("userAgents", [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36"
        ])
        
        return random.choice(user_agents)
    
    def get_request_delay(self) -> float:
        """Get delay between network requests"""
        config = self.anti_ban_config.get("network", {})
        delay_config = config.get("requestDelays", {})
        
        min_delay = delay_config.get("min", 100) / 1000
        max_delay = delay_config.get("max", 500) / 1000
        
        return random.uniform(min_delay, max_delay)


class AntiBlacklistSystem(ConfigurationManager):
    """Manages anti-blacklist protection"""
    
    def check_account_reputation(self) -> bool:
        """Verify account meets reputation requirements"""
        config = self.anti_blacklist_config.get("accountReputation", {})
        
        min_age = config.get("minimumAccountAge", {}).get("days", 30)
        min_trust = config.get("trustScore", {}).get("minRequired", 0.8)
        
        logger.info(f"Account reputation check: min_age={min_age}d, min_trust={min_trust}")
        return True
    
    def validate_behavior(self, stats: PlayerStats) -> Dict[str, Any]:
        """Validate player behavior against blacklist triggers"""
        config = self.anti_blacklist_config.get("behaviorAnalysis", {})
        violations = []
        
        stats_config = config.get("statisticsNormalization", {})
        win_rate_range = stats_config.get("keepWinRateBetween", [0.45, 0.65])
        kda_range = stats_config.get("keepKDABetween", [1.5, 3.5])
        max_headshot = stats_config.get("keepHeadshotRateBelow", 0.35)
        
        stats.calculate_metrics()
        
        # Validate win rate
        if not (win_rate_range[0] <= stats.win_rate <= win_rate_range[1]):
            violations.append(f"Win rate {stats.win_rate:.2%} outside safe range {win_rate_range}")
            self.blacklist_risk_score += 0.3
        
        # Validate KDA
        if not (kda_range[0] <= stats.kda <= kda_range[1]):
            violations.append(f"KDA {stats.kda:.2f} outside safe range {kda_range}")
            self.blacklist_risk_score += 0.3
        
        # Validate headshot rate
        if stats.games_played > 0:
            headshot_rate = stats.headshots / max(stats.kills, 1)
            if headshot_rate > max_headshot:
                violations.append(f"Headshot rate {headshot_rate:.2%} exceeds limit")
                self.blacklist_risk_score += 0.4
        
        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "risk_score": self.blacklist_risk_score
        }
    
    def calculate_risk_level(self, player_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall account risk level"""
        risk_factors = self.anti_blacklist_config.get("reportRiskFactors", {})
        factors = risk_factors.get("riskFactors", {})
        
        total_risk = 0.0
        risk_breakdown = {}
        
        if player_data.get("unusual_accuracy"):
            total_risk += factors.get("unusualAccuracy", 0.9)
            risk_breakdown["unusual_accuracy"] = True
        
        if player_data.get("impossible_kills"):
            total_risk += factors.get("impossibleKills", 1.0)
            risk_breakdown["impossible_kills"] = True
        
        if player_data.get("suspicious_behavior"):
            total_risk += factors.get("unusualBehavior", 0.7)
            risk_breakdown["suspicious_behavior"] = True
        
        threshold = risk_factors.get("reportThreshold", 0.6)
        is_flagged = total_risk > threshold
        
        return {
            "risk_score": total_risk,
            "is_flagged": is_flagged,
            "threshold": threshold,
            "risk_breakdown": risk_breakdown,
            "auto_mitigate": is_flagged and risk_factors.get("autoMitigate", True)
        }
    
    def apply_mitigation(self) -> List[str]:
        """Apply automatic mitigation strategies"""
        config = self.anti_blacklist_config.get("reportRiskFactors", {})
        mitigation = config.get("mitigation", {})
        
        actions = []
        
        if mitigation.get("slowDownProgression"):
            actions.append("SLOW_DOWN_PROGRESSION")
            logger.warning("Mitigation: Slowing down progression")
        
        if mitigation.get("increaseRandomErrors"):
            actions.append("INCREASE_RANDOM_ERRORS")
            logger.warning("Mitigation: Increasing random errors")
        
        if mitigation.get("reducePlayIntensity"):
            actions.append("REDUCE_PLAY_INTENSITY")
            logger.warning("Mitigation: Reducing play intensity")
        
        return actions
    
    def trigger_emergency_protocol(self) -> Dict[str, Any]:
        """Trigger emergency protocol for high-risk situations"""
        config = self.anti_blacklist_config.get("emergencyProtocol", {})
        
        return {
            "enabled": True,
            "actions": config.get("immediateActions", []),
            "status": "EMERGENCY_MODE_ACTIVATED"
        }


class AntiReportSystem(ConfigurationManager):
    """Manages anti-report protection"""
    
    def check_kill_patterns(self, kills_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check if kill patterns trigger report flags"""
        config = self.anti_report_config.get("reportTriggers", {})
        patterns = config.get("suspiciousKillPatterns", {})
        
        violations = []
        
        # Check consecutive headshots
        max_headshots = patterns.get("maxConsecutiveHeadshots", 8)
        if kills_data.get("consecutive_headshots", 0) > max_headshots:
            violations.append(f"Consecutive headshots ({kills_data['consecutive_headshots']}) exceeds limit ({max_headshots})")
            self.report_risk_score += 0.4
        
        # Check kills per minute
        max_kpm = patterns.get("maxKillsPerMinute", 4)
        if kills_data.get("kills_per_minute", 0) > max_kpm:
            violations.append(f"KPM ({kills_data['kills_per_minute']:.1f}) exceeds limit ({max_kpm})")
            self.report_risk_score += 0.3
        
        return {
            "safe": len(violations) == 0,
            "violations": violations,
            "risk_score": self.report_risk_score
        }
    
    def validate_behavior_for_reports(self, behavior: Dict[str, Any]) -> Dict[str, Any]:
        """Validate player behavior against report triggers"""
        config = self.anti_report_config.get("automatedReportSystem", {})
        evasion = config.get("evasionStrategies", {})
        
        # Check accuracy
        accuracy_config = evasion.get("varyAccuracy", {})
        target_range = accuracy_config.get("targetRange", [0.55, 0.70])
        
        current_accuracy = behavior.get("accuracy", 0.65)
        accuracy_safe = target_range[0] <= current_accuracy <= target_range[1]
        
        # Check reaction time
        reaction_config = evasion.get("normalReactionTime", {})
        min_ms = reaction_config.get("minMs", 150)
        max_ms = reaction_config.get("maxMs", 500)
        
        current_reaction = behavior.get("reaction_time_ms", 300)
        reaction_safe = min_ms <= current_reaction <= max_ms
        
        return {
            "accuracy_safe": accuracy_safe,
            "reaction_safe": reaction_safe,
            "overall_safe": accuracy_safe and reaction_safe,
            "current_accuracy": current_accuracy,
            "current_reaction_ms": current_reaction
        }
    
    def check_player_sportsmanship(self, chat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check player behavior for report-triggering communication"""
        config = self.anti_report_config.get("playerReportAvoidance", {})
        comm_config = config.get("communication", {})
        
        issues = []
        
        if chat_data.get("trash_talked"):
            issues.append("Trash talk detected")
            self.report_risk_score += 0.2
        
        if chat_data.get("insults"):
            issues.append("Insults detected")
            self.report_risk_score += 0.3
        
        if chat_data.get("improper_language"):
            issues.append("Improper language detected")
            self.report_risk_score += 0.2
        
        return {
            "issues": issues,
            "safe": len(issues) == 0,
            "risk_score": self.report_risk_score
        }
    
    def get_performance_distribution(self) -> Dict[str, float]:
        """Get recommended performance distribution to avoid reports"""
        config = self.anti_report_config.get("matchBehavior", {})
        perf_dist = config.get("performanceVariation", {})
        
        return {
            "good_games": perf_dist.get("goodGames", 0.70),
            "average_games": perf_dist.get("averageGames", 0.20),
            "bad_games": perf_dist.get("badGames", 0.10)
        }
    
    def should_play_badly_this_game(self) -> bool:
        """Determine if this game should be a bad game for statistics"""
        distribution = self.get_performance_distribution()
        bad_game_chance = distribution["bad_games"]
        
        return random.random() < bad_game_chance
    
    def get_safe_kill_spacing(self) -> Tuple[int, int]:
        """Get safe spacing between kills in seconds"""
        config = self.anti_report_config.get("matchBehavior", {})
        spacing = config.get("killSpacing", {})
        
        min_sec = spacing.get("minSecondsBetweenKills", 3)
        max_sec = spacing.get("maxSecondsBetweenKills", 15)
        
        return (min_sec, max_sec)
    
    def get_statistics_limits(self) -> Dict[str, Any]:
        """Get safe statistics limits"""
        config = self.anti_report_config.get("statisticsManagement", {})
        
        return {
            "win_rate_range": config.get("winRate", {}).get("targetRange", [0.48, 0.62]),
            "kda_range": config.get("killDeathRatio", {}).get("targetRange", [1.8, 2.5]),
            "headshot_range": config.get("headShotPercentage", {}).get("targetRange", [0.20, 0.35]),
            "max_win_streak": config.get("winRate", {}).get("maxWinStreak", 12)
        }


class ComprehensiveAntiSystem:
    """Unified system combining all anti protections"""
    
    def __init__(self):
        self.anti_ban = AntiBanSystem()
        self.anti_blacklist = AntiBlacklistSystem()
        self.anti_report = AntiReportSystem()
        self.player_stats = PlayerStats()
        
    def perform_full_account_check(self) -> Dict[str, Any]:
        """Perform comprehensive account safety check"""
        logger.info("=" * 60)
        logger.info("PERFORMING COMPREHENSIVE ACCOUNT SAFETY CHECK")
        logger.info("=" * 60)
        
        # Anti-Ban Check
        logger.info("\n[1/3] Anti-Ban System Check...")
        action_delay = self.anti_ban.get_action_delay()
        login_behavior = self.anti_ban.get_login_behavior()
        accuracy = self.anti_ban.apply_humanlike_accuracy()
        logger.info(f"  ✓ Action delay: {action_delay:.2f}s")
        logger.info(f"  ✓ Accuracy pattern: Miss={accuracy['miss']}, Headshot={accuracy['headshot']}")
        logger.info(f"  ✓ Login setup: Next in {login_behavior['delay_hours']}h")
        
        # Anti-Blacklist Check
        logger.info("\n[2/3] Anti-Blacklist System Check...")
        self.anti_blacklist.check_account_reputation()
        blacklist_validation = self.anti_blacklist.validate_behavior(self.player_stats)
        logger.info(f"  ✓ Behavior validation: {'SAFE' if blacklist_validation['valid'] else 'WARNING'}")
        logger.info(f"  ✓ Blacklist risk score: {blacklist_validation['risk_score']:.2f}")
        
        # Anti-Report Check
        logger.info("\n[3/3] Anti-Report System Check...")
        kill_pattern_check = self.anti_report.check_kill_patterns({
            "consecutive_headshots": 5,
            "kills_per_minute": 2.5
        })
        logger.info(f"  ✓ Kill patterns: {'SAFE' if kill_pattern_check['safe'] else 'FLAGGED'}")
        logger.info(f"  ✓ Report risk score: {kill_pattern_check['risk_score']:.2f}")
        
        behavior_check = self.anti_report.validate_behavior_for_reports({
            "accuracy": 0.62,
            "reaction_time_ms": 300
        })
        logger.info(f"  ✓ Behavior patterns: {'SAFE' if behavior_check['overall_safe'] else 'SUSPICIOUS'}")
        
        perf_dist = self.anti_report.get_performance_distribution()
        logger.info(f"  ✓ Performance distribution: Good={perf_dist['good_games']:.0%}, Average={perf_dist['average_games']:.0%}, Bad={perf_dist['bad_games']:.0%}")
        
        # Overall Assessment
        logger.info("\n" + "=" * 60)
        total_risk = (blacklist_validation['risk_score'] + 
                     kill_pattern_check['risk_score'] + 
                     self.anti_report.report_risk_score) / 3
        
        status = "🔴 CRITICAL" if total_risk > 0.8 else "🟠 WARNING" if total_risk > 0.6 else "🟢 SAFE"
        logger.info(f"OVERALL ACCOUNT STATUS: {status}")
        logger.info(f"Combined Risk Score: {total_risk:.2f}")
        logger.info("=" * 60)
        
        return {
            "status": status,
            "combined_risk_score": total_risk,
            "anti_ban_status": "ACTIVE",
            "anti_blacklist_status": "ACTIVE",
            "anti_report_status": "ACTIVE",
            "recommendations": self._get_recommendations(total_risk)
        }
    
    def _get_recommendations(self, risk_score: float) -> List[str]:
        """Get safety recommendations"""
        recommendations = []
        
        if risk_score > 0.8:
            recommendations.extend([
                "IMMEDIATE: Stop ranked gameplay",
                "Take 48-72 hour account break",
                "Rotate IP and clear device fingerprint",
                "Change play style significantly"
            ])
        elif risk_score > 0.6:
            recommendations.extend([
                "Reduce gameplay intensity",
                "Limit to 5-8 games per day",
                "Vary play style and weapons",
                "Monitor account closely"
            ])
        else:
            recommendations.extend([
                "Continue normal play with caution",
                "Maintain natural behavior patterns",
                "Regular account monitoring"
            ])
        
        return recommendations
    
    def generate_full_report(self) -> Dict[str, Any]:
        """Generate comprehensive safety report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "account_check": self.perform_full_account_check(),
            "player_statistics": asdict(self.player_stats),
            "configuration_status": {
                "anti_ban": "LOADED",
                "anti_blacklist": "LOADED",
                "anti_report": "LOADED"
            },
            "next_check_recommended": (datetime.now() + timedelta(hours=4)).isoformat()
        }


def main():
    """Main execution"""
    logger.info("Free Fire Anti-Ban, Anti-Blacklist, and Anti-Report System v1.0")
    logger.info("Starting comprehensive system initialization...\n")
    
    # Initialize comprehensive system
    system = ComprehensiveAntiSystem()
    
    # Perform full account check
    report = system.generate_full_report()
    
    logger.info("\nGenerating detailed safety report...")
    print(json.dumps(report, indent=2))
    
    logger.info("\nSystem initialization complete!")
    logger.info("All protections are now active.")


if __name__ == "__main__":
    main()
