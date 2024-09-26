import { Controller, Get, Res } from '@nestjs/common';
import { Response } from 'express';
import { join } from 'path';

@Controller()
export class HttpController {
  @Get()
  getIndex(@Res() res: Response) {
    res.sendFile(join(__dirname, '../..', 'public', 'index.html'));
  }

  @Get('chat')
  getChat(@Res() res: Response) {
    res.sendFile(join(__dirname, '../..', 'public', 'chat.html'));
  }

  @Get('grades')
  getGradesPage(@Res() res: Response) {
    res.sendFile(join(__dirname, '../..', 'public', 'grades.html'));
  }
}
