#!/usr/bin/env python3
"""
Saillent Governance Graph Generator (G3-1)
Generates board-ready visualizations, risk heatmaps, compliance trend
projections, and executive summary charts for AI governance reporting.
"""

import json
import argparse
from datetime import datetime, timedelta

class GovernanceGraphGenerator:
    """
    Saillent Graph Generator (G3-1)
    Produces data structures for executive visualizations:
    - Risk heatmaps
    - Compliance trend projections
    - Tier distribution charts
    - Regulatory timeline forecasts
    - Budget allocation recommendations
    """
    
    HEATMAP_COLORS = {
        "CRITICAL": "#dc2626",  # Red
        "HIGH": "#ea580c",      # Orange
        "MEDIUM": "#f59e0b",    # Amber
        "LOW": "#3aaa96",       # Teal/Saillent brand
        "COMPLIANT": "#22c55e"  # Green
    }
    
    def __init__(self, institution_name):
        self.institution = institution_name
        self.data_sources = {}
    
    def ingest_data(self, source_name, data):
        """Ingest data from any Saillent tool."""
        self.data_sources[source_name] = data
    
    def generate_heatmap(self):
        """Generate risk heatmap data for visualization."""
        heatmap = {
            "chart_type": "risk_heatmap",
            "title": "AI Governance Risk Heatmap",
            "generated_at": datetime.now().isoformat(),
            "axes": {
                "x": "Likelihood of Regulatory Finding",
                "y": "Financial Impact Severity"
            },
            "zones": []
        }
        
        if "shadow_ai" in self.data_sources:
            shadow = self.data_sources["shadow_ai"]
            for tool in shadow.get("tools", []):
                heatmap["zones"].append({
                    "label": tool.get("tool_name", "Unknown"),
                    "x": tool.get("breach_probability_pct", 0),
                    "y": tool.get("total_exposure", 0),
                    "risk_tier": tool.get("risk_tier", "LOW"),
                    "color": self.HEATMAP_COLORS.get(tool.get("risk_tier", "LOW"), "#3aaa96")
                })
        
        if "compliance" in self.data_sources:
            comp = self.data_sources["compliance"]
            for domain, scores in comp.get("domain_scores", {}).items():
                gap = scores.get("gap", 0)
                priority = scores.get("priority", "LOW")
                heatmap["zones"].append({
                    "label": domain,
                    "x": min(gap * 1.5, 100),
                    "y": gap * 10000,
                    "risk_tier": priority,
                    "color": self.HEATMAP_COLORS.get(priority, "#f59e0b")
                })
        
        return heatmap
    
    def generate_trend_projection(self, months=12):
        """Generate compliance trend projection data."""
        projection = {
            "chart_type": "trend_projection",
            "title": f"Compliance Trend Projection ({months} Months)",
            "generated_at": datetime.now().isoformat(),
            "months": months,
            "baseline": {},
            "projected": [],
            "target": 85
        }
        
        # Get current scores
        current_month = datetime.now()
        
        if "compliance" in self.data_sources:
            comp = self.data_sources["compliance"]
            overall = comp.get("overall_compliance", {})
            current_score = overall.get("overall_compliance_score", 50)
            
            projection["baseline"] = {
                "current_score": current_score,
                "current_month": current_month.strftime("%B %Y")
            }
            
            # Model improvement trajectory (logarithmic improvement curve)
            for i in range(months + 1):
                month_date = current_month + timedelta(days=30 * i)
                # Saillent Improvement Model: diminishing returns curve
                improvement = 35 * (1 - 2.71828 ** (-0.3 * i))
                projected_score = min(current_score + improvement, 98)
                
                projection["projected"].append({
                    "month": month_date.strftime("%B %Y"),
                    "month_index": i,
                    "projected_score": round(projected_score, 1),
                    "gap_to_target": round(max(projection["target"] - projected_score, 0), 1),
                    "status": "ON_TRACK" if projected_score >= 70 else "AT_RISK"
                })
        
        return projection
    
    def generate_tier_distribution(self):
        """Generate tier distribution data for pie/bar charts."""
        distribution = {
            "chart_type": "tier_distribution",
            "title": "Model Risk Tier Distribution",
            "generated_at": datetime.now().isoformat(),
            "tiers": {}
        }
        
        if "risk_engine" in self.data_sources:
            risk = self.data_sources["risk_engine"]
            matrix = risk.get("model_risk_matrix", [])
            
            tier_counts = {"TIER_1_CRITICAL": 0, "TIER_2_HIGH": 0, "TIER_3_MODERATE": 0, "TIER_4_LOW": 0}
            tier_revenue = {"TIER_1_CRITICAL": 0, "TIER_2_HIGH": 0, "TIER_3_MODERATE": 0, "TIER_4_LOW": 0}
            
            for model in matrix:
                tier = model.get("tier", "TIER_4_LOW")
                tier_counts[tier] = tier_counts.get(tier, 0) + 1
                tier_revenue[tier] = tier_revenue.get(tier, 0) + model.get("revenue_impact_millions", 0)
            
            colors = {
                "TIER_1_CRITICAL": self.HEATMAP_COLORS["CRITICAL"],
                "TIER_2_HIGH": self.HEATMAP_COLORS["HIGH"],
                "TIER_3_MODERATE": self.HEATMAP_COLORS["MEDIUM"],
                "TIER_4_LOW": self.HEATMAP_COLORS["LOW"]
            }
            
            for tier, count in tier_counts.items():
                distribution["tiers"][tier] = {
                    "count": count,
                    "revenue_impact_millions": round(tier_revenue[tier], 2),
                    "percentage": round((count / max(len(matrix), 1)) * 100, 1),
                    "color": colors.get(tier, "#3aaa96")
                }
        
        return distribution
    
    def generate_budget_recommendation(self):
        """Generate budget allocation recommendations for governance remediation."""
        budget = {
            "chart_type": "budget_allocation",
            "title": "Recommended Governance Budget Allocation",
            "generated_at": datetime.now().isoformat(),
            "total_annual_budget": 0,
            "allocations": [],
            "roi_projection": {}
        }
        
        if "compliance" in self.data_sources:
            comp = self.data_sources["compliance"]
            domains = comp.get("domain_scores", {})
            
            total_gap = sum(d.get("gap", 0) for d in domains.values())
            
            if total_gap > 0:
                # Base budget calculation
                base_budget = 250_000  # Minimum annual governance budget
                variable_budget = total_gap * 5000  # $5K per percentage point of gap
                total_budget = base_budget + variable_budget
                
                budget["total_annual_budget"] = round(total_budget, 2)
                
                for domain, scores in domains.items():
                    gap = scores.get("gap", 0)
                    if gap > 0:
                        allocation_pct = (gap / total_gap) * 100
                        amount = total_budget * (allocation_pct / 100)
                        
                        budget["allocations"].append({
                            "domain": domain,
                            "gap": gap,
                            "allocation_pct": round(allocation_pct, 1),
                            "annual_amount": round(amount, 2),
                            "priority": scores.get("priority", "MEDIUM"),
                            "expected_roi": f"{round(gap * 1.5)}% improvement within 6 months"
                        })
                
                budget["roi_projection"] = {
                    "annual_cost": round(total_budget, 2),
                    "regulatory_penalty_avoidance": round(total_budget * 3.5, 2),
                    "net_savings": round(total_budget * 2.5, 2),
                    "payback_period_months": 4
                }
        
        return budget
    
    def generate_full_report(self, filepath):
        """Generate complete graph data package for executive dashboard."""
        report = {
            "report_type": "Saillent Governance Graph Package",
            "model": "G3-1 (Graph Generator v1.0)",
            "institution": self.institution,
            "generated_at": datetime.now().isoformat(),
            "graphs": {
                "risk_heatmap": self.generate_heatmap(),
                "trend_projection": self.generate_trend_projection(),
                "tier_distribution": self.generate_tier_distribution(),
                "budget_recommendation": self.generate_budget_recommendation()
            },
            "executive_one_pager": self._generate_one_pager()
        }
        
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _generate_one_pager(self):
        """Generate executive one-pager summary."""
        heatmap = self.generate_heatmap()
        trend = self.generate_trend_projection()
        budget = self.generate_budget_recommendation()
        
        critical_zones = sum(1 for z in heatmap.get("zones", []) if z.get("risk_tier") in ("CRITICAL", "HIGH"))
        
        return {
            "headline": f"AI Governance Status: {trend['baseline'].get('current_score', 'N/A')}%",
            "critical_risks": critical_zones,
            "projected_12mo_score": trend["projected"][-1]["projected_score"] if trend["projected"] else "N/A",
            "recommended_budget": f"${budget['total_annual_budget']:,.0f}",
            "expected_roi": f"${budget['roi_projection'].get('net_savings', 0):,.0f}",
            "next_board_review": (datetime.now() + timedelta(days=90)).strftime("%B %d, %Y"),
            "top_3_actions": [
                "Complete Shadow AI detection deployment",
                "Engage independent model validator for high-risk models",
                "Implement real-time audit trail monitoring"
            ]
        }

def main():
    parser = argparse.ArgumentParser(description="Saillent Graph Generator (G3-1)")
    parser.add_argument("--institution", required=True, help="Financial institution name")
    parser.add_argument("--shadow-report", help="Shadow AI exposure report JSON")
    parser.add_argument("--compliance-report", help="Compliance scoring report JSON")
    parser.add_argument("--risk-report", help="Risk engine report JSON")
    parser.add_argument("--output", default="governance_graphs.json", help="Output file")
    parser.add_argument("--demo", action="store_true", help="Run with demo data")
    args = parser.parse_args()
    
    print(f"\n📊 Saillent Graph Generator (G3-1)")
    print(f"   Institution: {args.institution}\n")
    
    g3 = GovernanceGraphGenerator(args.institution)
    
    if args.demo:
        # Load demo data from sibling tools
        demo_shadow = {
            "tools": [
                {"tool_name": "ChatGPT Free", "breach_probability_pct": 45, "total_exposure": 8500000, "risk_tier": "HIGH"},
                {"tool_name": "Claude Pro", "breach_probability_pct": 72, "total_exposure": 15200000, "risk_tier": "CRITICAL"},
                {"tool_name": "Gemini Personal", "breach_probability_pct": 28, "total_exposure": 2100000, "risk_tier": "MEDIUM"},
                {"tool_name": "Midjourney", "breach_probability_pct": 8, "total_exposure": 45000, "risk_tier": "LOW"}
            ]
        }
        
        demo_compliance = {
            "overall_compliance": {"overall_compliance_score": 55.6},
            "domain_scores": {
                "Governance & Oversight": {"gap": 13, "priority": "LOW"},
                "Model Inventory": {"gap": 35, "priority": "HIGH"},
                "Risk Assessment": {"gap": 37, "priority": "HIGH"},
                "Monitoring": {"gap": 42, "priority": "CRITICAL"},
                "Training": {"gap": 15, "priority": "MEDIUM"}
            }
        }
        
        demo_risk = {
            "model_risk_matrix": [
                {"tier": "TIER_1_CRITICAL", "revenue_impact_millions": 450},
                {"tier": "TIER_1_CRITICAL", "revenue_impact_millions": 800},
                {"tier": "TIER_2_HIGH", "revenue_impact_millions": 600},
                {"tier": "TIER_3_MODERATE", "revenue_impact_millions": 120},
                {"tier": "TIER_4_LOW", "revenue_impact_millions": 35},
                {"tier": "TIER_4_LOW", "revenue_impact_millions": 20}
            ]
        }
        
        g3.ingest_data("shadow_ai", demo_shadow)
        g3.ingest_data("compliance", demo_compliance)
        g3.ingest_data("risk_engine", demo_risk)
        print("   ✅ Demo data loaded from 3 Saillent modules\n")
    else:
        if args.shadow_report:
            with open(args.shadow_report) as f:
                g3.ingest_data("shadow_ai", json.load(f))
        if args.compliance_report:
            with open(args.compliance_report) as f:
                g3.ingest_data("compliance", json.load(f))
        if args.risk_report:
            with open(args.risk_report) as f:
                g3.ingest_data("risk_engine", json.load(f))
    
    report = g3.generate_full_report(args.output)
    
    one_pager = report["executive_one_pager"]
    budget = report["graphs"]["budget_recommendation"]
    
    print(f"📊 Executive One-Pager")
    print(f"   {one_pager['headline']}")
    print(f"   Critical Risks: {one_pager['critical_risks']}")
    print(f"   Projected 12-Month Score: {one_pager['projected_12mo_score']}%")
    print(f"   Recommended Budget: {one_pager['recommended_budget']}")
    print(f"   Expected ROI: {one_pager['expected_roi']}")
    
    print(f"\n💰 Budget Allocation:")
    for alloc in budget.get("allocations", []):
        print(f"   {alloc['domain']}: ${alloc['annual_amount']:,.0f} ({alloc['allocation_pct']}%)")
    
    print(f"\n📋 Top 3 Actions:")
    for action in one_pager["top_3_actions"]:
        print(f"   → {action}")
    
    print(f"\n📅 Next Board Review: {one_pager['next_board_review']}")

if __name__ == "__main__":
    main()
