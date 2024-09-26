import { Controller } from '@nestjs/common';
import { MessagePattern } from '@nestjs/microservices';

@Controller()
export class TcpController {
  @MessagePattern('calculate')
  calculate(data: any): any {
    const { operation, params } = data;
    let result;

    switch (operation) {
      case 'pythagoras':
        result = Math.sqrt(params.a ** 2 + params.b ** 2);
        break;
      case 'quadratic':
        const { a, b, c } = params;
        const discriminant = b ** 2 - 4 * a * c;
        if (discriminant < 0) {
          result = 'Нет действительных корней';
        } else {
          const x1 = (-b + Math.sqrt(discriminant)) / (2 * a);
          const x2 = (-b - Math.sqrt(discriminant)) / (2 * a);
          result = { x1, x2 };
        }
        break;
      case 'trapezoid_area':
        result = ((params.a + params.b) / 2) * params.h;
        break;
      case 'parallelogram_area':
        result = params.base * params.height;
        break;
      default:
        result = 'Неизвестная операция';
    }

    return result;
  }
}
