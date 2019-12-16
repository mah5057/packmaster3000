import { Component, OnInit } from '@angular/core';
import { Headers, Http, RequestOptions } from '@angular/http';

@Component({
  selector: 'packmaster',
  templateUrl: '../templates/packmaster.component.html'
})

export class PackMaster implements OnInit {

  private headers = new Headers({});
  private serverUrl: string;
  private apiUrl: string;

  duration: number;
  temperature: number;
  luxury: number;
  bonus: string;
  packlist: object;

  constructor(private http: Http) {
    this.serverUrl = window.location.origin;
    this.apiUrl = window.location.origin + '/api';
  }

  ngOnInit() {
    this.duration = null;
    this.temperature = null;
    this.luxury = null;
    this.bonus = null;
    this.packlist = null;
  }

  setPacklist(data: object) {
    this.packlist = data;
  }

  getPacklist() {
    let body = { 'duration': this.duration, 'temperature': this.temperature, 'luxury': this.luxury, 'bonus': this.bonus }
    return this.http.post(`${this.apiUrl}/packlist`, body, new RequestOptions({headers: this.headers}))
      .toPromise()
      .then(response => {
        let data = response.json();
        this.setPacklist(data);
      }).catch(this.handleError);
  }

  private handleError (error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
