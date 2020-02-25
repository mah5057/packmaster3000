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
    if(this.validateAll()) {
      let body = {
        'duration': this.duration,
        'temperature': this.temperature,
        'luxury': this.luxury,
        'bonus': this.bonus
      }
      return this.http.post(`${this.apiUrl}/packlist`, body, new RequestOptions({headers: this.headers}))
        .toPromise()
        .then(response => {
          let data = response.json();
          this.setPacklist(data);
        }).catch(this.handleError);
    }
  }

  validateAll() {
    if (!this.validateDuration() || !this.validateTemperature() || !this.validateLuxury()) {
      return false;
    }
    return true;
  }

  validateDuration() {
    if(!this.duration) {
      new alert("Duration is empty!");
      return false;
    }
    return true;
  }

  validateTemperature() {
    if(!this.temperature) {
      new alert("Temperature is empty!");
      return false;
    }
    return true;
  }

  validateLuxury() {
    if(!this.luxury) {
      new alert("Luxury is empty!");
      return false;
    }
    return true;
  }

  private handleError (error: any): Promise<any> {
    console.error('An error occurred', error);
    return Promise.reject(error.message || error);
  }
}
