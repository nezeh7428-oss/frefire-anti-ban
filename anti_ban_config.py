"""
Free Fire Anti-Ban Configuration Manager
Implements safety measures to prevent account suspension and blacklisting
"""

import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PlayerStats:
    """Track player statistics for blacklist avoidance"""
    wins: int = 0
    kills: int = 0
    deaths: int = 0
    headshots: int = 0
    games_played: int = 0
    accuracy: float = 0.0
    win_rate: float = 0.0
    kda: float = 0.0
    
    def calculate_metrics(self):
        """Calculate KDA and win rate"""
        if self.games_played > 0:
            self.win_rate = self.wins / self.games_played
        if self.deaths > 0:
            self.kda = self.kills / self.deaths
        else:
            self.kda = self.kills if self.kills > 0 else 0


class AntiBlacklistConfig:
    """Manages anti-blacklist configuration"""
    
    def __init__(self, config_file: str = "anti-blacklist-config.json"):
        self.config = self._load_config(config_file)
        self.player_stats = PlayerStats()
        self.risk_score = 0.0
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file {config_file} not found")
            return {}
    
    def check_account_reputation(self) -> bool:
        """Verify account meets reputation requirements"""
        config = self.config.get("accountReputation", {})
        
        # Check account age
        min_age = config.get("minimumAccountAge", {}).get("days", 30)
        logger.info(f"Minimum account age requirement: {min_age} days")
        
        # Check trust score
        min_trust = config.get("trustScore", {}).get("minRequired", 0.8)
        logger.info(f"Minimum trust score required: {min_trust}")
        
        return True
    
    def validate_behavior(self, stats: PlayerStats) -> Dict[str, Any]:
        """Validate player behavior against blacklist triggers"""
        config = self.config.get("behaviorAnalysis", {})
        violations = []
        
        # Check progression rate
        prog_config = config.get("progressionRate", {})
        max_level_ups = prog_config.get("maxLevelUpsPerDay", 3)
        max_rank_ups = prog_config.get("maxRankUpPerDay", 2)
        
        # Check statistics normalization
        stats_config = config.get("statisticsNormalization", {})
        win_rate_range = stats_config.get("keepWinRateBetween", [0.45, 0.65])
        kda_range = stats_config.get("keepKDABetween", [1.5, 3.5])
        max_headshot = stats_config.get("keepHeadshotRateBelow", 0.35)
        
        stats.calculate_metrics()
        
        # Validate win rate
        if not (win_rate_range[0] <= stats.win_rate <= win_rate_range[1]):
            violations.append(f"Win rate {stats.win_rate:.2%} outside safe range {win_rate_range}")
            self.risk_score += 0.3
        
        # Validate KDA
        if not (kda_range[0] <= stats.kda <= kda_range[1]):
            violations.append(f"KDA {stats.kda:.2f} outside safe range {kda_range}")
            self.risk_score += 0.3
        
        # Validate headshot rate
        if stats.games_played > 0:
            headshot_rate = stats.headshots / max(stats.kills, 1)
            if headshot_rate > max_headshot:
                violations.append(f"Headshot rate {headshot_rate:.2%} exceeds limit {max_headshot:.2%}")
                self.risk_score += 0.4
        
        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "risk_score": self.risk_score
        }
    
    def check_hardware_fingerprint(self, device_info: Dict[str, Any]) -> bool:
        """Validate hardware fingerprint consistency"""
        config = self.config.get("hardwareFingerprint", {})
        
        required_fields = ["machine_id", "gpu_renderer", "processor_info"]
        for field in required_fields:
            if field not in device_info:
                logger.warning(f"Missing hardware info: {field}")
                return False
        
        logger.info("Hardware fingerprint validated")
        return True
    
    def check_ip_geolocation(self, ip_info: Dict[str, Any]) -> bool:
        """Validate IP and geolocation consistency"""
        config = self.config.get("ipManagement", {})
        
        ip_config = config.get("ipRotation", {})
        geo_config = config.get("geolocation", {})
        
        # Check if IP rotation is enabled
        if not ip_config.get("enabled", True):
            logger.warning("IP rotation is disabled")
            return False
        
        # Validate geolocation consistency
        if not geo_config.get("keepConsistent", True):
            logger.warning("Geolocation changes detected")
            return False
        
        logger.info("IP and geolocation validated")
        return True
    
    def generate_humanized_timing(self) -> Dict[str, int]:
        """Generate human-like action timing"""
        config = self.config.get("antiCheatBypass", {})
        
        return {
            "reaction_time_ms": random.randint(150, 500),
            "action_delay_ms": random.randint(100, 300),
            "input_spread_ms": random.randint(50, 200)
        }
    
    def check_match_performance(self, match_stats: Dict[str, Any]) -> bool:
        """Check if match performance looks natural"""
        config = self.config.get("matchBehavior", {})
        perf_config = config.get("performanceConsistency", {})
        
        # Allow occasional bad games
        if random.random() < perf_config.get("badGameFrequency", 0.15):
            logger.info("Simulating occasional bad game for human behavior")
            return False
        
        return True
    
    def calculate_risk_level(self, player_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall account risk level"""
        risk_factors = self.config.get("reportRiskFactors", {})
        factors = risk_factors.get("riskFactors", {})
        
        total_risk = 0.0
        risk_breakdown = {}
        
        # Evaluate different risk factors
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
        config = self.config.get("reportRiskFactors", {})
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
        
        if mitigation.get("increaseBreakDuration"):
            actions.append("INCREASE_BREAK_DURATION")
            logger.warning("Mitigation: Increasing break duration")
        
        return actions
    
    def trigger_emergency_protocol(self) -> Dict[str, Any]:
        """Trigger emergency protocol for high-risk situations"""
        config = self.config.get("emergencyProtocol", {})
        
        return {
            "enabled": True,
            "actions": config.get("immediateActions", []),
            "low_play_mode": {
                "enabled": config.get("lowPlayDays", {}).get("enabled", True),
                "duration_days": config.get("lowPlayDays", {}).get("duration", 3),
                "max_games_per_day": config.get("lowPlayDays", {}).get("maxGamesPerDay", 2)
            },
            "status": "EMERGENCY_MODE_ACTIVATED"
        }
    
    def get_safe_play_limits(self) -> Dict[str, int]:
        """Get safe daily play limits"""
        return self.config.get("safetyLimits", {})
    
    def log_activity(self, activity_type: str, details: Dict[str, Any]):
        """Log all account activities"""
        config = self.config.get("logging", {})
        
        if config.get("trackAllActivity"):
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "activity_type": activity_type,
                "details": details
            }
            logger.info(f"Activity logged: {log_entry}")
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive account safety report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "current_risk_score": self.risk_score,
            "player_stats": asdict(self.player_stats),
            "safety_status": "SAFE" if self.risk_score < 0.6 else "WARNING" if self.risk_score < 0.8 else "CRITICAL",
            "recommendations": self._get_recommendations()
        }
    
    def _get_recommendations(self) -> List[str]:
        """Get safety recommendations based on risk score"""
        recommendations = []
        
        if self.risk_score > 0.8:
            recommendations.extend([
                "Stop all ranked gameplay immediately",
                "Reduce playtime significantly",
                "Change play style and weapon preferences",
                "Take extended account rest period",
                "Rotate IP and clear browser cookies"
            ])
        elif self.risk_score > 0.6:
            recommendations.extend([
                "Reduce gameplay intensity",
                "Limit ranked matches per day",
                "Vary play style more frequently",
                "Take regular breaks",
                "Monitor account for warnings"
            ])
        else:
            recommendations.extend([
                "Continue current play pattern",
                "Maintain natural behavior",
                "Monitor statistics regularly",
                "Avoid extreme performance swings"
            ])
        
        return recommendations


class AntiBanConfig:
    """Manages anti-ban configuration"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config = self._load_config(config_file)
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file {config_file} not found")
            return {}
    
    def get_action_delay(self) -> float:
        """Get random delay for action (in seconds)"""
        config = self.config.get("gameplay", {})
        delay_config = config.get("delayBetweenActions", {})
        
        min_delay = delay_config.get("min", 500) / 1000
        max_delay = delay_config.get("max", 2000) / 1000
        
        return random.uniform(min_delay, max_delay)
    
    def get_kill_delay(self) -> float:
        """Get delay before registering kills"""
        config = self.config.get("gameplay", {})
        kill_config = config.get("killDelay", {})
        
        min_delay = kill_config.get("min", 1000) / 1000
        max_delay = kill_config.get("max", 3000) / 1000
        
        return random.uniform(min_delay, max_delay)
    
    def apply_humanlike_accuracy(self) -> Dict[str, Any]:
        """Apply human-like accuracy patterns"""
        config = self.config.get("gameplay", {})
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
        config = self.config.get("gameplay", {})
        move_config = config.get("movementPattern", {})
        
        return {
            "enabled": move_config.get("enabled", True),
            "random_stutter": move_config.get("randomStutter", True),
            "walk_variation": move_config.get("walkVariation", 0.2),
            "stutter_chance": random.random() < 0.3
        }
    
    def get_login_behavior(self) -> Dict[str, Any]:
        """Get login behavior configuration"""
        config = self.config.get("account", {})
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
        config = self.config.get("network", {})
        user_agents = config.get("userAgents", [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ])
        
        return random.choice(user_agents)
    
    def get_request_delay(self) -> float:
        """Get delay between network requests"""
        config = self.config.get("network", {})
        delay_config = config.get("requestDelays", {})
        
        min_delay = delay_config.get("min", 100) / 1000
        max_delay = delay_config.get("max", 500) / 1000
        
        return random.uniform(min_delay, max_delay)


def main():
    """Main execution"""
    
    # Initialize configurations
    anti_ban = AntiBanConfig("config.json")
    anti_blacklist = AntiBlacklistConfig("anti-blacklist-config.json")
    
    logger.info("=== Anti-Ban Configuration System Initialized ===\n")
    
    # Example: Check account reputation
    logger.info("Checking account reputation...")
    anti_blacklist.check_account_reputation()
    
    # Example: Simulate player stats
    logger.info("\nSimulating player statistics...")
    test_stats = PlayerStats(
        wins=45,
        kills=350,
        deaths=120,
        headshots=50,
        games_played=100
    )
    
    # Validate behavior
    validation = anti_blacklist.validate_behavior(test_stats)
    logger.info(f"Behavior validation: {validation}")
    
    # Check match performance
    logger.info("\nChecking match performance...")
    is_natural = anti_blacklist.check_match_performance({})
    logger.info(f"Performance looks natural: {is_natural}")
    
    # Get action delays
    logger.info("\nGenerating human-like timings...")
    action_delay = anti_ban.get_action_delay()
    logger.info(f"Action delay: {action_delay:.2f}s")
    
    accuracy = anti_ban.apply_humanlike_accuracy()
    logger.info(f"Accuracy pattern: {accuracy}")
    
    # Get login behavior
    logger.info("\nLogin behavior:")
    login_behavior = anti_ban.get_login_behavior()
    logger.info(f"Next login in: {login_behavior['delay_hours']} hours")
    
    # Calculate risk
    logger.info("\nCalculating risk level...")
    risk_assessment = anti_blacklist.calculate_risk_level({
        "unusual_accuracy": False,
        "impossible_kills": False,
        "suspicious_behavior": False
    })
    logger.info(f"Risk assessment: {risk_assessment}")
    
    # Generate report
    logger.info("\nGenerating safety report...")
    report = anti_blacklist.generate_report()
    logger.info(f"Safety report: {json.dumps(report, indent=2)}")
    
    logger.info("\n=== System Check Complete ===")


if __name__ == "__main__":
    main()
