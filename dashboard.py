#!/usr/bin/env python3
"""
Governance Dashboard — Saillent
Board-ready AI governance dashboard generator for financial institutions.
Aggregates model inventory, risk assessments, audit readiness, and compliance
status into a single executive view aligned with OSFI E-23 and SR 11-7.
"""

import json
import argparse
from datetime import datetime, timedelta
from collections import defaultdict

class GovernanceDashboard:
    """Executive AI governance dashboard."""
    
    def __init__(self, institution_name):
        self.institution = institution_name
        self.generated_at = datetime.now().isoformat()
        self.metrics = {}
        self.alerts = []
        self.compliance = {}
        self.board_summary = {}
    
    def ingest_inventory(self, inventory_file):
        """Ingest model inventory data."""
        with open(inventory_file) as f:
            data = json.load(f)
        
        summary = data.get("summary", {})
        self.metrics["model_inventory"] = {
            "total_models": summary.get("total_models", 0),
            "registered_models": summary.get("registered_models", 0),
            "shadow_ai_models": summary.get("shadow_ai_models", 0),
            "completeness": round((summary.get("registered_models", 0) / max(summary.get("total_models", 1), 1)) * 100, 1)
        }
        
        if summary.get("shadow_ai_models", 0) > 0:
            self.alerts.append({
                "severity": "HIGH",
                "source": "Model Inventory",
                "message": f"{summary['shadow_ai_models']} Shadow AI models detected — immediate governance review required",
                "regulatory_ref": "OSFI E-23 §2.3 / SR 11-7"
            })
    
    def ingest_risk_assessment(self, risk_file):
        """Ingest risk assessment data."""
        with open(risk_file) as f:
            data = json.load(f)
        
        domains = data.get("domains", [])
        scores = {d["domain"]: d["score"] for d in domains}
        
        self.metrics["risk_assessment"] = {
            "overall_score": data.get("overall_score", 0),
            "readiness_level": data.get("readiness_level", "UNKNOWN"),
            "domain_scores": scores,
            "critical_gaps": len([d for d in domains if d["score"] < 40])
        }
        
        for gap in data.get("gap_analysis", []):
            self.alerts.append({
                "severity": gap.get("severity", "ELEVATED"),
                "source": f"Risk Assessment — {gap['domain']}",
                "message": gap["impact"],
                "regulatory_ref": "SR 11-7 / OCC Guidance"
            })
    
    def ingest_audit_status(self, audit_file):
        """Ingest audit trail status."""
        with open(audit_file) as f:
            data = json.load(f)
        
        audit_log = data.get("audit_log", {})
        entries = data.get("entries", [])
        
        self.metrics["audit_readiness"] = {
            "total_entries": audit_log.get("total_entries", 0),
            "chain_verified": audit_log.get("chain_verified", False),
            "last_entry": entries[-1]["timestamp"] if entries else None,
            "coverage_days": self._calculate_coverage(entries)
        }
        
        if not audit_log.get("chain_verified", False):
            self.alerts.append({
                "severity": "CRITICAL",
                "source": "Audit Trail",
                "message": "Audit chain integrity compromised — immediate investigation required",
                "regulatory_ref": "SEC Rule 17a-4 / OSFI E-23 §4.3"
            })
    
    def _calculate_coverage(self, entries):
        """Calculate audit trail coverage in days."""
        if not entries:
            return 0
        timestamps = [e["timestamp"] for e in entries if "timestamp" in e]
        if len(timestamps) < 2:
            return 1
        first = datetime.fromisoformat(timestamps[0])
        last = datetime.fromisoformat(timestamps[-1])
        return (last - first).days
    
    def generate_dashboard(self):
        """Generate the complete executive dashboard."""
        high_alerts = [a for a in self.alerts if a["severity"] in ("CRITICAL", "HIGH")]
        medium_alerts = [a for a in self.alerts if a["severity"] == "MEDIUM"]
        
        overall_compliance = 0
        components = 0
        
        if "model_inventory" in self.metrics:
            overall_compliance += self.metrics["model_inventory"]["completeness"]
            components += 1
        if "risk_assessment" in self.metrics:
            overall_compliance += self.metrics["risk_assessment"]["overall_score"]
            components += 1
        if "audit_readiness" in self.metrics:
            overall_compliance += (100 if self.metrics["audit_readiness"]["chain_verified"] else 50)
            components += 1
        
        overall_score = round(overall_compliance / max(components, 1), 1)
        
        dashboard = {
            "dashboard_type": "AI Governance Executive Dashboard",
            "institution": self.institution,
            "generated_at": self.generated_at,
            "framework": "OSFI E-23 / SR 11-7",
            "overall_compliance_score": overall_score,
            "rating": self._get_rating(overall_score),
            "metrics": self.metrics,
            "alerts": {
                "critical": len(high_alerts),
                "elevated": len(medium_alerts),
                "total": len(self.alerts),
                "details": self.alerts[:20]
            },
            "board_summary": self._generate_board_summary(overall_score),
            "regulatory_readiness": self._regulatory_checklist(),
            "recommended_actions": self._generate_actions(high_alerts)
        }
        
        return dashboard
    
    def _get_rating(self, score):
        if score >= 90:
            return "GREEN — Well-governed"
        elif score >= 70:
            return "YELLOW — Moderate gaps"
        elif score >= 50:
            return "ORANGE — Significant exposure"
        else:
            return "RED — Critical regulatory risk"
    
    def _generate_board_summary(self, score):
        return {
            "headline": f"AI Governance Score: {score}%",
            "key_message": self._get_rating(score),
            "top_3_priorities": [a["message"] for a in sorted(self.alerts, key=lambda x: x["severity"])[:3]],
            "next_board_review": (datetime.now() + timedelta(days=90)).strftime("%B %d, %Y"),
            "regulatory_outlook": "OSFI examinations intensifying. SR 11-7 enforcement increasing. Prepare for formal review within 6 months."
        }
    
    def _regulatory_checklist(self):
        return [
            {"regulation": "OSFI E-23", "status": "In Progress", "deadline": "Ongoing"},
            {"regulation": "SR 11-7", "status": "In Progress", "deadline": "Ongoing"},
            {"regulation": "SEC Reg S-ID", "status": "Applicable", "deadline": "As required"},
            {"regulation": "CFPB Fair Lending", "status": "Applicable", "deadline": "Ongoing"},
            {"regulation": "FINRA AI Oversight", "status": "Applicable", "deadline": "As required"},
            {"regulation": "GDPR/CCPA AI Provisions", "status": "Review", "deadline": "As applicable"},
        ]
    
    def _generate_actions(self, high_alerts):
        actions = []
        for alert in high_alerts[:5]:
            actions.append({
                "priority": alert["severity"],
                "action": alert["message"],
                "owner": "Chief Risk Officer",
                "timeline": "7 days" if alert["severity"] == "CRITICAL" else "14 days",
                "saillent_support": "Available for immediate engagement"
            })
        return actions

def main():
    parser = argparse.ArgumentParser(description="Saillent Governance Dashboard")
    parser.add_argument("--institution", required=True, help="Financial institution name")
    parser.add_argument("--inventory", help="Model inventory JSON file")
    parser.add_argument("--risk", help="Risk assessment JSON file")
    parser.add_argument("--audit", help="Audit trail JSON file")
    parser.add_argument("--output", default="governance_dashboard.json", help="Output JSON file")
    parser.add_argument("--demo", action="store_true", help="Run with demo data")
    args = parser.parse_args()
    
    print(f"\n📊 Saillent AI Governance Dashboard")
    print(f"   Institution: {args.institution}")
    print(f"   Framework: OSFI E-23 / SR 11-7\n")
    
    dashboard = GovernanceDashboard(args.institution)
    
    if args.demo:
        # Generate demo files
        import tempfile, os
        
        demo_inventory = {
            "summary": {"total_models": 47, "registered_models": 42, "shadow_ai_models": 5}
        }
        demo_risk = {
            "overall_score": 68.5,
            "readiness_level": "DEVELOPING",
            "domains": [
                {"domain": "Model Inventory", "score": 78.0},
                {"domain": "Risk Assessment", "score": 62.0},
                {"domain": "Independent Validation", "score": 55.0},
                {"domain": "Ongoing Monitoring", "score": 45.0},
                {"domain": "Board Governance", "score": 81.0}
            ],
            "gap_analysis": [
                {"domain": "Ongoing Monitoring", "severity": "CRITICAL", "impact": "No real-time monitoring — 45% score indicates immediate regulatory exposure"},
                {"domain": "Independent Validation", "severity": "ELEVATED", "impact": "Validation coverage below SR 11-7 expectations"}
            ]
        }
        demo_audit = {
            "audit_log": {"total_entries": 1250, "chain_verified": True},
            "entries": [{"timestamp": "2026-05-01T00:00:00Z"}, {"timestamp": "2026-05-12T00:00:00Z"}]
        }
        
        # Write temp files
        for name, data in [("inv", demo_inventory), ("risk", demo_risk), ("audit", demo_audit)]:
            path = f"/tmp/demo_{name}.json"
            with open(path, "w") as f:
                json.dump(data, f)
        
        dashboard.ingest_inventory("/tmp/demo_inv.json")
        dashboard.ingest_risk_assessment("/tmp/demo_risk.json")
        dashboard.ingest_audit_status("/tmp/demo_audit.json")
        print("   ✅ Demo data loaded: 47 models, 68.5% risk score, 1,250 audit entries\n")
    else:
        if args.inventory:
            dashboard.ingest_inventory(args.inventory)
        if args.risk:
            dashboard.ingest_risk_assessment(args.risk)
        if args.audit:
            dashboard.ingest_audit_status(args.audit)
    
    report = dashboard.generate_dashboard()
    
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"📊 Executive Dashboard")
    print(f"   Overall Score: {report['overall_compliance_score']}%")
    print(f"   Rating: {report['rating']}")
    print(f"   🔴 Critical Alerts: {report['alerts']['critical']}")
    print(f"   🟡 Elevated Alerts: {report['alerts']['elevated']}")
    print(f"   Output: {args.output}\n")
    
    print("📋 Top Priorities for Board:")
    for priority in report["board_summary"]["top_3_priorities"]:
        print(f"   → {priority}")
    
    print(f"\n📅 Next Board Review: {report['board_summary']['next_board_review']}")

if __name__ == "__main__":
    main()
