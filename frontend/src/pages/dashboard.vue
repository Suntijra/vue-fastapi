<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>ขอคิวใหม่</v-card-title>
            <v-card-text>
              <v-form ref="form" v-model="valid">
                <v-text-field
                  v-model="licensePlate"
                  :rules="[rules.required]"
                  label="หมายเลขทะเบียนรถ"
                  required
                ></v-text-field>
                <v-select
                  v-model="selectedGate"
                  :items="gates.map(gate => gate.type)"
                  :rules="[rules.required]"
                  label="เลือกประเภทประตู"
                  required
                ></v-select>
                <v-btn @click="requestQueue">ขอคิว</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col v-for="(gate, index) in gates" :key="index" cols="12" md="4">
          <v-card>
            <v-card-title>{{ gate.type }} (ประตู {{ gate.count }})</v-card-title>
            <v-card-text>
              <v-data-table :headers="headers" :items="queueData[index]" class="elevation-1"></v-data-table>
            </v-card-text>
            <v-card-actions>
              <v-btn @click="callNextVehicle(index)">เรียกรถเข้า</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
  
      <!-- ตารางสถานะของรถ -->
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>สถานะของรถ</v-card-title>
            <v-card-text>
              <v-data-table :headers="statusHeaders" :items="statusData" class="elevation-1" @click:row="selectRow"></v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
  
      <!-- Dropdown เปลี่ยนสถานะ -->
      <v-dialog v-model="dialog" max-width="300px">
        <v-card>
          <v-card-title class="headline">เปลี่ยนสถานะ</v-card-title>
          <v-card-text>
            <v-select v-model="selectedStatus" :items="statusOptions" label="เลือกสถานะ"></v-select>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="updateStatus" color="primary">บันทึก</v-btn>
            <v-btn @click="dialog = false">ยกเลิก</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  
      <v-row>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>สถิติการโหลดของ</v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>จำนวนรถที่เข้า: {{ totalVehicles }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>เวลาที่ใช้ในการโหลด (เฉลี่ย): {{ averageLoadingTime }} นาที</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>กราฟแนวโน้มการเข้าออกของรถ</v-card-title>
            <v-card-text>
              <v-chart :data="chartData"></v-chart>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      
      <v-alert v-if="nextQueue" type="info">
        คิวถัดไป: {{ nextQueue.licensePlate }} เวลา: {{ nextQueue.time }}
      </v-alert>
    </v-container>
  </template>
  
  <script>
  export default {
    data() {
      return {
        licensePlate: '',
        selectedGate: null,
        valid: false,
        rules: {
          required: value => !!value || 'จำเป็นต้องกรอก'
        },
        gates: [
          { type: 'ประเภทที่ 1 (รถ 10 ล้อ)', count: 2 },
          { type: 'ประเภทที่ 2 (รถ 6 ล้อ)', count: 4 },
          { type: 'ประเภทที่ 3 (รถกระบะ)', count: 2 }
        ],
        headers: [
          { text: 'หมายเลขรถ', value: 'licensePlate' },
          { text: 'เวลาเรียกคิว', value: 'time' }
        ],
        statusHeaders: [
          { text: 'หมายเลขรถ', value: 'licensePlate' },
          { text: 'สถานะ', value: 'status' },
          { text: 'เวลาอัปเดต', value: 'updatedAt' }
        ],
        queueData: [[], [], []],
        statusData: [],
        nextQueue: null,
        totalVehicles: 0,
        averageLoadingTime: 0,
        chartData: {
          labels: [],
          datasets: [{
            label: 'จำนวนรถที่เข้า',
            data: []
          }],
        },
        dialog: false,
        selectedStatus: '',
        selectedRow: null,
        statusOptions: ['รอเรียก', 'เรียกรถเข้า', 'เสร็จสิ้น', 'ยกเลิก']
      };
    },
    methods: {
      requestQueue() {
        const gateIndex = this.gates.findIndex(gate => gate.type === this.selectedGate);
        const timeNow = new Date().toLocaleString();
        if (gateIndex !== -1 && this.licensePlate) {
          this.queueData[gateIndex].push({
            licensePlate: this.licensePlate,
            time: timeNow
          });
  
          // Update status data
          this.updateStatusData(this.licensePlate, 'รอเรียก', timeNow);
          
          // Update total vehicles and average loading time
          this.totalVehicles++;
          this.averageLoadingTime = this.calculateAverageLoadingTime();
  
          // Update chart data
          this.updateChartData();
  
          this.licensePlate = '';
          this.selectedGate = null;
          this.$refs.form.reset();
        }
      },
      callNextVehicle(gateIndex) {
        const vehicle = this.queueData[gateIndex].shift();
        if (vehicle) {
          this.nextQueue = vehicle;
          this.updateStatusData(vehicle.licensePlate, 'เรียกรถเข้า', new Date().toLocaleString());
        }
      },
      updateStatusData(licensePlate, status, time) {
        console.log(licensePlate, status, time)
        const index = this.statusData.findIndex(item => item.licensePlate === licensePlate);
        if (index !== -1) {
          this.statusData[index].status = status;
          this.statusData[index].updatedAt = time;
        } else {
          this.statusData.push({
            licensePlate,
            status,
            updatedAt: time
          });
        }
      },
      selectRow(item) {
        this.selectedRow = item; // เก็บข้อมูลแถวที่เลือก
        this.selectedStatus = item.status; // กำหนดสถานะที่เลือกไว้
        this.dialog = true; // แสดง dialog เปลี่ยนสถานะ
      },
      updateStatus() {
        if (this.selectedRow) {
          const timeNow = new Date().toLocaleString();
          this.updateStatusData(this.selectedRow.licensePlate, this.selectedStatus, timeNow);
          this.dialog = false; // ปิด dialog
        }
      },
      calculateAverageLoadingTime() {
        return Math.floor(Math.random() * 10) + 1; // เปลี่ยนเป็นค่าจริงตามข้อมูลที่มี
      },
      updateChartData() {
        const currentDate = new Date().toLocaleDateString();
        this.chartData.labels.push(currentDate);
        this.chartData.datasets[0].data.push(this.totalVehicles);
      }
    }
  };
  </script>
  