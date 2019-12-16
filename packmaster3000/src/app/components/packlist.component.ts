import { Component, Input } from '@angular/core';

@Component({
  selector: 'packlist',
  templateUrl: '../templates/packlist.component.html'
})

export class PackList {

  @Input() packlistData: object;
}
