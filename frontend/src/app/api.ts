import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Vulnerability {
  id: number;
  software_name: string;
  affected_version: string;
  cve_id: string;
  severity: string;
  patch_command: string;
  published_date: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  getVulnerabilities(): Observable<Vulnerability[]> {
    return this.http.get<Vulnerability[]>(`${this.apiUrl}/vulnerabilities`);
  }

  getStatus(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/status`);
  }

  scanNow(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/scan`);
  }
}
