import { Component, OnInit, OnDestroy } from '@angular/core';
import { Headers, Http, RequestOptions } from '@angular/http';
import { Location }               from '@angular/common';

@Component({
  selector: 'packmaster',
  templateUrl: './packmaster.component.html'
})

export class PackMaster implements OnInit {

  private headers = new Headers({});
  private serverUrl: string;
  private apiUrl: string;

  duration: number;
  temperature: number;
  luxury: number;
  bonus: string;

  constructor(private http: Http) {
    this.serverUrl = window.location.origin;
    this.apiUrl = window.location.origin + '/api';
  }

  ngOnInit() {
    this.duration = null;
    this.temperature = null;
    this.luxury = null;
    this.bonus = null;
  }

  getPresentation() {
    let body = { 'duration': this.duration, 'temperature': this.temperature, 'luxury': this.luxury, 'bonus': this.bonus }
    return this.http.post(`${this.apiUrl}/packlist`, body, new RequestOptions({headers: this.headers}))
      .toPromise()
      .then(response => {
        let data = response.json().result;
        return data;
      }).catch(this.handleError);
  }

  private handleError (error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
