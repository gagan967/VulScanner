import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Vulnerability } from '../api';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export class DashboardComponent implements OnInit {
  vulnerabilities: Vulnerability[] = [];
  status: any = {};
  isLoading = true;

  constructor(private api: ApiService) { }

  ngOnInit(): void {
    this.refreshData();
  }

  severityCounts = { critical: 0, high: 0, medium: 0, low: 0 };

  allVulnerabilities: Vulnerability[] = [];
  currentFilter: string = 'ALL';

  refreshData() {
    this.isLoading = true;
    this.api.getVulnerabilities().subscribe(data => {
      this.allVulnerabilities = data;
      this.calculateStats();
      this.applyFilter();
      this.isLoading = false;
    });
    this.api.getStatus().subscribe(s => this.status = s);
  }

  calculateStats() {
    this.severityCounts = { critical: 0, high: 0, medium: 0, low: 0 };
    this.allVulnerabilities.forEach(v => {
      const s = v.severity?.toLowerCase();
      if (s === 'critical') this.severityCounts.critical++;
      else if (s === 'high') this.severityCounts.high++;
      else if (s === 'medium') this.severityCounts.medium++;
      else this.severityCounts.low++;
    });
  }

  filterBy(severity: string) {
    this.currentFilter = severity;
    this.applyFilter();
  }

  applyFilter() {
    if (this.currentFilter === 'ALL') {
      this.vulnerabilities = [...this.allVulnerabilities];
    } else {
      this.vulnerabilities = this.allVulnerabilities.filter(v =>
        v.severity?.toUpperCase() === this.currentFilter
      );
    }
  }

  getSeverityColor(severity: string): string {
    switch (severity?.toUpperCase()) {
      case 'CRITICAL': return 'text-red-600 bg-red-100';
      case 'HIGH': return 'text-orange-600 bg-orange-100';
      case 'MEDIUM': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  }

  openPatch(v: Vulnerability) {
    const cmd = v.patch_command || '';

    // Logic: Mock Professional Patching
    if (cmd.startsWith('Mock Fix:')) {
      const parts = cmd.replace('Mock Fix: ', '').split('|');
      const url = parts[0];
      const instructions = parts[1] || 'Follow standard procedures.';

      const message = `
🔧 OFFICIAL PATCH AVAILABLE

SOURCE: ${url}

INSTRUCTIONS:
${instructions}

(Click OK to copy download link)
      `;

      if (confirm(message)) {
        navigator.clipboard.writeText(url);
        window.open('about:blank', '_blank');
      }
      return;
    }

    // 1. If we have a direct Manual Fix URL from the scanner, use it.
    if (cmd.startsWith('Manual Fix:')) {
      const url = cmd.replace('Manual Fix: ', '').trim();
      window.open(url, '_blank');
      return;
    }

    // 2. Fallback: Search for the latest version download
    const query = `${v.software_name} download latest version official`;
    const url = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
    window.open(url, '_blank');
  }
}
