import {
  Controller,
  Get,
  Param,
  Delete,
  UseGuards,
  Patch,
} from '@nestjs/common';
import { Roles } from '@/src/auth/decorators/roles.decorator';
import { JwtAuthGuard } from '@/src/auth/guards/jwt-auth.guard';
import { UsersService } from '@/src/users/users.service';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @UseGuards(JwtAuthGuard)
  @Roles('admin')
  @Get()
  async findAll() {
    return this.usersService.findAll();
  }

  @UseGuards(JwtAuthGuard)
  @Roles('admin')
  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.usersService.findOneById(+id);
  }

  @UseGuards(JwtAuthGuard)
  @Roles('admin')
  @Patch(':id/block')
  async blockUser(@Param('id') id: string) {
    return this.usersService.blockUser(+id);
  }

  @UseGuards(JwtAuthGuard)
  @Roles('admin')
  @Delete(':id')
  async remove(@Param('id') id: string) {
    return this.usersService.remove(+id);
  }
}
